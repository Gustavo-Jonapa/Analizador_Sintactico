from flask import Flask, render_template,request,redirect,url_for
from lexer import build_lexer,lexer_errors as lex_errors_global
from parser import parse_input,parse_errors as parse_errors_global
import lexer as lexmod

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", lex_results=None, lex_errors=None, syn_result=None, syn_errors=None)

@app.route("/lex", methods=["POST"])
def analyze_lex():
    code = request.form.get("code", "")
    lexer = build_lexer()
    lexer.input(code)

    tokens = []
    while True:
        tok = lexer.token()
        if not tok: break

        row = {
            "token": tok.value,
            "reservada": "",
            "identificador": "",
            "numero": "",
            "simbolo": ""
        }

        if tok.type in ["FOR", "WHILE", "IF", "SYSTEM", "PRINT"]:
            row["reservada"] = "X"
        elif tok.type == "ID":
            row["identificador"] = "X"
        elif tok.type == "NUMBER":
            row["numero"] = "X"
        elif tok.type in ["PLUSPLUS", "PLUSEQ", "EQUALS", "LE", "LT", "GE", "GT", "EQEQ",
                          "PLUS", "MINUS", "TIMES", "DIVIDE",
                          "LPAREN", "RPAREN", "LBRACE", "RBRACE",
                          "SEMI", "COMMA", "DOT"]:
            row["simbolo"] = "X"

        tokens.append(row)

    lex_errors = lexmod.lexer_errors.copy()
    return render_template(
        "index.html",
        lex_results=tokens,
        lex_errors=lex_errors,
        syn_result=None,
        syn_errors=None,
        code=code
    )

@app.route("/syn", methods=["POST"])
def analyze_syn():
    code = request.form.get("code", "")
    ast, errors = parse_input(code)
    lex_errors = lexmod.lexer_errors.copy()
    return render_template("index.html", lex_results=None, lex_errors=lex_errors, syn_result=ast, syn_errors=errors, code=code)

if __name__ == "__main__":
    app.run(debug=True)