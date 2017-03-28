# @app.route("/postData", methods=['POST'])
# def postData():
#     page_url = request.form.get('page')
#     # c = CodechefProblemPage.getCodechefProblem(page_url)
#     # print 'Got problem: ' + c.name
#     # result = predict.predict(c)
#     return jsonify({'Status': str(78)})
__author__ = 'Pranay'
from flask import Flask, request, jsonify, json, render_template

import  sys
# sys.path.append("../Data Extraction/codechef/")
# sys.path.append("../Data Extraction/Codeforces/")
# sys.path.append("../Data Extraction/SPOJ/")
# import predictCategory, problems, CodeforcesProblem, spojProblem
print 'import complete'
app = Flask(__name__)

@app.route('/')
def index():
   return 'Hello World'

@app.route("/getData", methods=['GET'])
def getData():

    entry2Value = request.args.get('entry2_id')
    entry1Value = request.args.get('entry1_id')

    var1 = int(entry2Value) + int(entry1Value)
    var2 = 10
    var3 = 15
    print entry1Value
    return jsonify({ 'var1': var1, 'var2': var2, 'var3': var3 })


@app.route("/postData", methods=['POST'])
def postData():
    platform_url = request.form.get('url')
    problem_content = request.form.get('content')
    if platform_url == 'www.codechef.com':
        c = problems.getProblemFromDescription(problem_content)
    elif platform_url == 'codeforces.com':
        c = CodeforcesProblem.getProblemFromDescription(problem_content)
    else:
        c = spojProblem.getProblemFromDescription(problem_content)
    result = predictCategory.predict_category(c)
    return jsonify({'result':result})

@app.route("/profile/<name>")
def profile(name):
    username = name
    probsSolved = {"Easy":33, "Medium":5, "Hard":1}
    categorySolved = {"String":8, "Maths":11, "Dp":5, "Graph":8, "Trees":7}
    totalSolved = 39
    recommended_probs = [{"name":"prob1",
                          "link":"https://www.codechef.com/problems/KOL16F",
                          "category":"string",
                          "diff":"medium"},
                         {"name":"prob2",
                          "link":"https://www.codechef.com/problems/RSERVER",
                          "category":"dp",
                          "diff":"medium"},
                         {"name":"prob3",
                          "link":"https://www.codechef.com/problems/KOL1502",
                          "category":"graph",
                          "diff":"medium"},
                         ]
    user = {
        "name":username.upper(),
        "totalSolved":totalSolved,
        "probsSolved":probsSolved,
        "categorySolved":categorySolved,
        "recommended_probs":recommended_probs
        }
    return render_template("profile.html", user=user)

# app.run(debug=True)
if __name__ == '__main__':
    print 'Starting'
    app.run(debug=True)