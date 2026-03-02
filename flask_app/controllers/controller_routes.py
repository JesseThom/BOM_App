from flask import render_template, redirect, request, flash, Response
from flask_app import app
from flask_app.models.model_options import Option
from flask_app.models.model_jobs import Job
from flask_app.models.model_tags import Tag
from werkzeug.utils import secure_filename
from datetime import datetime, timezone
# import csv

#landing page
@app.route('/')
def landing_page():
    jobs= Job.get_all()
    # user = request.environ.get("REMOTE_USER")
    # if not user:
    #     user = "Jthommes"
    return render_template("index.html",jobs=jobs)

#new job
@app.route('/new_job')
def new_job():
    return render_template('job_new.html')

#create job
@app.route('/create_job', methods=['post'])
def create_job():
    data=request.form
    if not Job.job_check(data):
        return redirect('/')
    Job.create(data)
    return redirect('/')


#new tag
@app.route('/tag/<int:job_id>')
def new_tag(job_id):
    options = Option.get_all()
    return render_template("tag_new.html",job_id=job_id,options=options)

#create tag
@app.route('/create_tag',methods=["post"])
def create_tag():
    data = request.form
    if not Tag.validate(data):
        print("duplicate handle")
        return redirect(f'/tag/{data['job_id']}')
    Tag.create(data)
    return redirect(f'/BOM/{data["job_id"]}')

#edit tag
@app.route('/edit_tag/<int:id>')
def edit_tag(id):
    tag = Tag.get_one({"id":id})
    options = Option.get_all()
    return render_template('tag_edit.html',tag=tag,options=options)

#submit tag edit
@app.route('/update_tag',methods=["post"])
def update_tag():
    data = request.form
    Tag.update_one(data)
    return redirect(f'/BOM/{data["job_id"]}')

#remove tag
@app.route('/remove_tag/<int:job_id>/<int:id>')
def remove_tag(job_id,id):
    Tag.remove_one({'id':id})
    return redirect(f'/BOM/{job_id}')

#reinstate tag
@app.route('/reinstate_tag/<int:job_id>/<int:id>')
def reinstate_tag(job_id,id):
    Tag.reinstate_one({'id':id})
    return redirect(f'/BOM/{job_id}')

#delete tag
@app.route('/delete_tag/<int:job_id>/<int:id>')
def delete_tag(job_id,id):
    Tag.delete_one({'id':id})
    return redirect(f'/BOM/{job_id}')

# main Bom page
@app.route('/BOM/<int:job_id>')
def bom(job_id):
    tags = Tag.get_all_main({"job_id":job_id})
    job = Job.get_one({'id':job_id})
    return render_template('main.html',job=job,tags=tags,now=datetime.now())

# controls temp route
@app.route('/controls/<int:job_id>')
def controls(job_id):
    tags = Tag.get_all({"job_id":job_id})
    job = Job.get_one({'id':job_id})
    return render_template('controls.html',job=job,tags=tags,now=datetime.now())
#controls page
# @app.route('/controls/<int:job_id>')
# def controls(job_id):
#     results = Tag.everything({"id":job_id})
#     job = Job.get_one({'id':job_id})
    
#     tags = {}``

#     for row in results:
#         opt_id = row.id
    
#         if opt_id not in tags:
#             tags[opt_id] = {
#                 "id": opt_id,
#                 "type": row.type,
#                 "tag_number": row.tag_number,
#                 "desc": row.option_desc,
#                 "option_desc":row.option_desc,
#                 "process_desc":row.process_desc,
#                 "control_panel": row.control_panel,
#                 "electrical": row.electrical,
#                 "a_i":row.a_i,
#                 "a_o":row.a_o,
#                 "d_i":row.d_i,
#                 "d_o":row.d_o,
#                 "devices": []
#             }

#         tags[opt_id]["devices"].append({
#             "mod_num": row.model_number,
#             "man": row.man,
#             "qty": row.qty
#         })
#     return render_template("controls.html",job=job,tags= tags.values())

#process page
@app.route('/process/<int:job_id>')
def process(job_id):
    tags = Tag.get_all({"job_id":job_id})
    job = Job.get_one({'id':job_id})
    
    # tags = {}

    # for row in results:
    #     opt_id = row.id
    
    #     if opt_id not in tags:
    #         tags[opt_id] = {
    #             "id": opt_id,
    #             "type": row.type,
    #             "tag_number": row.tag_number,
    #             "desc": row.option_desc,
    #             "p_desc": row.process_desc,
    #             "devices": []
    #         }

    #     tags[opt_id]["devices"].append({
    #         "mod_num": row.model_number,
    #         "man": row.man,
    #         "qty": row.qty
    #     })
    return render_template("process.html",job=job,tags= tags,now=datetime.now())

#design page
@app.route('/design/<int:job_id>')
def design(job_id):
    results = Tag.get_everything({"job_id":job_id})
    job = Job.get_one({'id':job_id})
    
    tags = {}

    for row in results:
        opt_id = row.id
    
        if opt_id not in tags:
            tags[opt_id] = {
                "id": opt_id,
                "type": row.type,
                "tag_number": row.tag_number,
                "desc": row.option_desc,
                "process_desc": row.process_desc,
                "control_panel": row.control_panel,
                "active": row.active,
                "updated_at": row.updated_at,
                "devices": []
            }

        tags[opt_id]["devices"].append({
            "mod_num": row.model_number,
            "man": row.man,
            "qty": row.qty,
            "order_status": row.order_status,
            "por_number": row.por_number
        })
    return render_template("design.html",job=job,tags= tags.values(),now=datetime.now())

# import from acad 
@app.route("/job/<int:job_id>/import_tags", methods=["GET"])
def import_tags_page(job_id):
    job = Job.get_one({'id':job_id})
    return render_template("import_tags.html", job=job)

# parse and import acad
@app.route("/job/<int:job_id>/import_tags", methods=["POST"])
def import_tags(job_id):
    # raw = request.form["raw_text"]
    # lines = raw.strip().splitlines()

    file = request.files.get("acad_file")

    if not file or file.filename == "":
        # flash("No file selected")
        return redirect(request.url)

    # filename = secure_filename(file.filename)

    raw = file.read().decode("utf-8", errors="ignore")
    lines = raw.strip().splitlines()

    imported = 0
    skipped = 0

    for line in lines:
        if not line.strip():
            continue

        cols = line.split("\t")

        if len(cols) < 4:
            skipped += 1
            continue

        if cols[0].upper() == "HANDLE":
            continue

        handle = cols[0].strip().lstrip("'")
        blockname = cols[1].strip()
        type = cols[2].strip()
        number = cols[3].strip()

        # prevent duplicates on same job
        exists = Tag.get_one_by_handle({'handle':handle})
        if exists:
            skipped += 1
            continue

        tag = {
            'job_id':job_id,
            'handle':handle,
            'blockname':blockname,
            'type':type,
            'tag_number':number,
            'process_desc':"",
            'option_id':1
        }

        Tag.create(tag)

    flash(f"Duplicate Handle, skipped {skipped}")
    flash (f"Created {imported}")
    return redirect(f"/controls/{job_id}")

@app.route('/job/<int:job_id>/exports')
def exports(job_id):
    return render_template('exports.html', job_id=job_id)

