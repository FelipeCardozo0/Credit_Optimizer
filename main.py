from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from credit_model import analyze_credit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.route('/', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            app.config['UPLOAD_FOLDER'],
            secure_filename(file.filename)
        )
        file.save(file_path)

        try:
            # Process the file
            output_path = analyze_credit(file_path)
            return redirect(url_for('results', filename=os.path.basename(output_path)))
        except UnicodeDecodeError:
            os.remove(file_path)  # Cleanup the invalid file
            return "Error: Unable to read the file. Ensure it's encoded in UTF-8 or Latin-1."
        except ValueError as e:
            os.remove(file_path)  # Cleanup the invalid file
            return f"Error: {e}"

    return render_template('index.html', form=form)



@app.route('/results/<filename>')
def results(filename):
    file_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return render_template('results.html', file_url=file_url)


@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
