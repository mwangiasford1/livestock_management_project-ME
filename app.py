from flask import Flask, request, jsonify

app = Flask(__name__)  # ✅ Initialize Flask properly

@app.route('/')
def home():
    return jsonify({"message": "🚀 Livestock Management System API is running!"})

if __name__ == '__main__':
    print("🚀 Flask server is starting... Visit http://127.0.0.1:5000/")
    app.run(debug=True, host='0.0.0.0', port=5000)

@app.route('/livestock/<rfid_tag>', methods=['GET'])
def get_livestock_by_rfid(rfid_tag):
    db = get_livestock_by_rfid_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM livestock WHERE rfid_tag = %s", (rfid_tag,))
    data = cursor.fetchone()
    
    cursor.close()
    db.close()
    
    return jsonify(data if data else {"message": "⚠️ Livestock not found"})
