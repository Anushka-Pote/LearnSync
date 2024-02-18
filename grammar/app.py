from flask import Flask, render_template, request
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# Registering custom extension 'is_correction' if not already registered
if not spacy.tokens.Token.has_extension('is_correction'):
    spacy.tokens.Token.set_extension('is_correction', default=False)

def correct_grammar(passage):
    doc = nlp(passage)
    corrected_passage = ' '.join([token.text_with_ws if not token._.get('is_correction') else token._.get('suggestion', '') for token in doc])
    return corrected_passage

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        passage = request.form['passage']
        corrected_passage = correct_grammar(passage)
        return render_template('index.html', passage=passage, corrected_passage=corrected_passage)
    else:
        return render_template('index.html', passage='', corrected_passage='')

if __name__ == '__main__':
    app.run(debug=True)
