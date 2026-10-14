
from flask import Flask, request, render_template_string
from transformers import pipeline

app = Flask(__name__)

print("Loading NLP model... Please wait.")

generator = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

print("Model loaded successfully!")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Automatic News Headline Generator</title>
    <style>
        body {
            font-family: Arial;
            background: #eef2f7;
            margin: 40px;
        }
        .container {
            max-width: 750px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 12px;
        }
        h1 { color: #153b65; }
        textarea {
            width: 98%;
            height: 220px;
            padding: 8px;
        }
        button {
            background: #1769aa;
            color: white;
            padding: 12px 20px;
            border: none;
            cursor: pointer;
        }
        .result {
            background: #e1f5e8;
            padding: 15px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Automatic News Headline Generator</h1>
    <p>Enter a news article below.</p>
    <form method="POST">
        <textarea name="article"
        placeholder="Paste your news article here..."
        required>{{ article }}</textarea>
        <br><br>
        <button type="submit">Generate Headline</button>
    </form>
    {% if headline %}
    <div class="result">
        <h3>Generated Headline / Summary</h3>
        <p>{{ headline }}</p>
    </div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    article = ""
    headline = ""

    if request.method == "POST":
        article = request.form.get("article", "").strip()

        if len(article.split()) < 20:
            headline = "Please enter a longer article (at least 20 words)."
        else:
            try:
                result = generator(
                    article,
                    max_length=40,
                    min_length=8,
                    do_sample=False,
                    truncation=True
                )
                headline = result[0]["summary_text"]
            except Exception as error:
                headline = "Generation error: " + str(error)

    return render_template_string(
        HTML, article=article, headline=headline
    )

if __name__ == "__main__":
    app.run(debug=False, port=5000)
