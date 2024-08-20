import sqlite3
import json


def update_ship(id, ship_data):
    with sqlite3.connect("./shipping.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Ship
                SET
                    name = ?,
                    hauler_id = ?
            WHERE id = ?
            """,
            (ship_data["name"], ship_data["hauler_id"], id),
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False


def delete_ship(pk):
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        DELETE FROM Ship WHERE id = ?
        """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def list_ships(url):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        if url["query_params"]["_expand"]:
            db_cursor.execute(
                """
            SELECT
                s.id,
                s.name,
                s.hauler_id,
                h.id haulerId,
                h.name haulerName,
                h.dock_id
            FROM Ship s
            JOIN Hauler h
                ON h.id = s.hauler_id
            """
            )

        else:
            db_cursor.execute(
                """
            SELECT
                s.id,
                s.name,
                s.hauler_id
            FROM Ship s
            """
            )
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        ships = []

        for row in query_results:
            hauler = {
                "id": row["haulerId"],
                "name": row["haulerName"],
                "dock_id": row["dock_id"],
            }
            ship = {
                "id": row["id"],
                "name": row["name"],
                "hauler_id": row["hauler_id"],
                "hauler": hauler,
            }
            ships.append(ship)

        # Serialize Python list to JSON encoded string
        serialized_ships = json.dumps(ships)

    return serialized_ships


def retrieve_ship(url, pk):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        if url["query_params"]["_expand"]:
            db_cursor.execute(
                """
            SELECT
                s.id,
                s.name,
                s.hauler_id,
                h.id haulerId,
                h.name haulerName,
                h.dock_id
            FROM Ship s
            JOIN Hauler h
                ON h.id = s.hauler_id
            WHERE s.id = ?
            """,
                (pk,),
            )
        else:
            db_cursor.execute(
                """
            SELECT
                s.id,
                s.name,
                s.hauler_id
            FROM Ship s
            WHERE s.id = ?
            """,
                (pk,),
            )
        query_results = db_cursor.fetchone()

        # Initialize the ship dictionary
        if url["query_params"]["_expand"]:
            hauler = {
                "id": query_results["haulerId"],
                "name": query_results["haulerName"],
                "dock_id": query_results["dock_id"],
            }
            ship = {
                "id": query_results["id"],
                "name": query_results["name"],
                "hauler_id": query_results["hauler_id"],
                "hauler": hauler,
            }
        else:
            ship = {
                "id": query_results["id"],
                "name": query_results["name"],
                "hauler_id": query_results["hauler_id"],
            }

        # Serialize Python dictionary to JSON encoded string
        serialized_ship = json.dumps(ship)

    return serialized_ship


def create_ship(ship_data):
    with sqlite3.connect("./shipping.db") as conn:
        db_cursor = conn.cursor()

        # Write the SQL query to insert the new ship
        db_cursor.execute(
            """
            INSERT INTO Ship (name, hauler_id)
            VALUES (?, ?)
            """,
            (ship_data["name"], ship_data["hauler_id"]),
        )

        # Commit the transaction
        conn.commit()

        # Get the ID of the newly inserted ship
        new_ship_id = db_cursor.lastrowid

    # Return the ID of the newly created ship
    return new_ship_id
