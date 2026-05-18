from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ====================== LISTA DE CPFs AUTORIZADOS ======================
# CADASTRE AQUI OS CPFs DAS PESSOAS QUE PODEM USAR O SISTEMA
# O CPF deve ser o MESMO que você colocar dentro do elo.py
AUTHORIZED_CPFS = {
    "15503080901": {  # ← CPF da pessoa 1
        "name": "Joao Silva",
        "expires": "2026-12-31",
        "active": True
    },
    "98765432100": {  # ← CPF da pessoa 2
        "name": "Maria Santos",
        "expires": "2027-12-31",
        "active": True
    },
    # ADICIONE MAIS CPFs AQUI CONFORME NECESSARIO
}

@app.route('/verify', methods=['POST'])
def verify_access():
    try:
        data = request.get_json()
        cpf = data.get('cpf', '').strip()
        cpf = ''.join(filter(str.isdigit, cpf))
        
        if cpf in AUTHORIZED_CPFS:
            user_info = AUTHORIZED_CPFS[cpf]
            
            # Verifica se esta ativo
            if not user_info.get("active", True):
                return jsonify({
                    "authorized": False,
                    "message": "Acesso bloqueado"
                })
            
            # Verifica se expirou
            if user_info.get("expires"):
                exp_date = datetime.strptime(user_info["expires"], "%Y-%m-%d")
                if datetime.now() > exp_date:
                    return jsonify({
                        "authorized": False,
                        "message": "Licenca expirada"
                    })
            
            return jsonify({
                "authorized": True,
                "name": user_info["name"],
                "expires": user_info["expires"]
            })
        else:
            return jsonify({
                "authorized": False,
                "message": "CPF nao autorizado"
            })
    except Exception as e:
        return jsonify({"authorized": False, "message": str(e)})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "online"})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)