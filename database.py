def add_livestock(tag_id, name, breed, age, weight, health_status):
    db = connect_db()
    cursor = db.cursor()

    # Check if the tag_id already exists
    cursor.execute("SELECT COUNT(*) FROM livestock WHERE tag_id = %s", (tag_id,))
    if cursor.fetchone()[0] > 0:
        print(f"⚠️ Error: RFID {tag_id} already exists!")
    else:
        query = """
            INSERT INTO livestock (tag_id, name, breed, age, weight, health_status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (tag_id, name, breed, age, weight, health_status))
        db.commit()
        print(f"✅ {name} added successfully!")

    cursor.close()
    db.close()
