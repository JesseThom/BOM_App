from flask import render_template, redirect, request, flash, Response
from flask_app import app
from flask_app.models.model_options import Option
from flask_app.models.model_jobs import Job
from flask_app.models.model_tags import Tag
from werkzeug.utils import secure_filename
from datetime import datetime, timezone

# Electrical Export
@app.route("/job/<int:job_id>/electrical")
def electrical(job_id):
    job = Job.get_one({"id": job_id})
    return render_template("electrical.html", job=job)

@app.route("/job/<int:job_id>/export", methods=["POST"])
def export_export(job_id):
    data = {
        "job_id": job_id,
        "control_panel": request.form.get("control_panel"),
        "selected_ios" : request.form.getlist("io")
    }
    rows = Tag.export_test(data)

    def generate():
        csv_columns = ["Full Tag", "process_desc","option_desc","control_panel", "a_i","a_o","d_i","d_o"]

        if not rows:
            return

        # CSV Header
        yield ",".join(csv_columns) + "\n"

        for row in rows:
            print(row)
            full_tag = f"{row['type']}-{row['tag_number']}"

            values = [
                full_tag,
                row['process_desc'] or "",
                row['option_desc'] or "",
                row['control_panel'] or "",
                row['a_i'] or "",
                row['a_o'] or "",
                row['d_i'] or "",
                row['d_o'] or ""
            ]
            yield ",".join(map(str, values)) + "\n"
            # yield ",".join([str(row.get(col) or "") for col in csv_columns]) + "\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            f"attachment; filename=job_{job_id}_export.csv"
        }
    )

# POR Export
@app.route("/job/<int:job_id>/por")
def por(job_id):
    job = Job.get_one({"id": job_id})
    return render_template("por_new.html", job=job)

# @app.route("/job/<int:job_id>/por")
# def por(job_id):
#     job = Job.get_one({"id": job_id})
#     return render_template("por_new.html", job=job)