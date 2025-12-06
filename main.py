from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # للسماح بالطلبات من نطاقات مختلفة

# بيانات جواز سفر وهمية
mock_passport_data = {
    "1081142444": {
        "status": "success",
        "data": {
            "fullName": "محمد أحمد العتيبي",
            "nationalId": "1105112345",
            "passportNumber": "P1234567",
            "issueDate": "2022-03-15",
            "expiryDate": "2027-03-15",
            "nationality": "سعودي",
            "dateOfBirth": "1990-05-10",
            "status": "صالح",
            "issuingAuthority": "مديرية جوازات الرياض"
        }
    },
    "1081142455": {
        "status": "success",
        "data": {
            "fullName": "خالد سعود الفهد",
            "nationalId": "1105223344",
            "passportNumber": "P7654321",
            "issueDate": "2023-01-20",
            "expiryDate": "2028-01-20",
            "nationality": "سعودي",
            "dateOfBirth": "1985-11-15",
            "status": "صالح",
            "issuingAuthority": "مديرية جوازات جدة"
        }
    }
}

@app.route('/api/passport/v1/<national_id>', methods=['GET'])
def get_passport_info(national_id):
    """استرجاع معلومات جواز السفر باستخدام الرقم الوطني"""
    
    if national_id in mock_passport_data:
        return jsonify(mock_passport_data[national_id])
    else:
        return jsonify({
            "status": "error",
            "message": "لم يتم العثور على معلومات جواز سفر لهذا الرقم الوطني",
            "code": "404"
        }), 404

@app.route('/api/passport/v1/verify-passport/<passport_number>', methods=['GET'])
def verify_passport(passport_number):
    """التحقق من صحة جواز السفر"""
    
    for citizen_id, data in mock_passport_data.items():
        if data["data"]["passportNumber"] == passport_number:
            verification_result = {
                "status": "success",
                "isValid": True,
                "passportNumber": passport_number,
                "fullName": data["data"]["fullName"],
                "expiryDate": data["data"]["expiryDate"]
            }
            return jsonify(verification_result)
    
    return jsonify({
        "status": "error",
        "isValid": False,
        "message": "جواز السفر غير موجود أو غير صالح"
    }), 404

@app.route('/', methods=['GET'])
def health_check():
    """فحص حالة الخدمة"""
    return jsonify({
        "status": "healthy",
        "service": "جوازات وهمية",
        "version": "1.0.0",
        "timestamp": "2024-01-15T10:30:00Z"
    })

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
