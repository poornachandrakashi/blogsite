import datetime

def xray_submit():
    image = request.files['image']
    ts = time.gmtime()
    uploadtime = time.strftime("%Y%m%d%H%M%S", ts)
    filename = "image" + uploadtime + ".jpg"
    filename = os.path.join('static/images/articles/',filename)
    app.logger.info("File to upload: ")
    app.logger.info(filename)
    image.save(filename)
    return render_template('xray-submit.html', image = "static/images/result/"+destination_file1, result = result)