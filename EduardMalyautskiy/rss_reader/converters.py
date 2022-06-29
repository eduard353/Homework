from jinja2 import Environment, FileSystemLoader
import datetime
from fpdf import FPDF, HTMLMixin
from os import path
from urllib.parse import urlparse
from progress.bar import Bar
import json



class PDF(FPDF, HTMLMixin):
    pass


def get_file_local_path(url):
    local_path = path.join(path.abspath(path.dirname(__file__)), 'images', path.basename(urlparse(url).path))

    return local_path


def convert_to_html(data, local=False):
    """
    Function for generating HTML from a list of articles.

    :param data: list of articles in dict format
    :param local: flag of source data. False - Internet, True - cache DB
    :return: HTML in string
    """

    env = Environment(
        loader=FileSystemLoader(path.join(path.abspath(path.dirname(__file__)), "templates")),

    )

    template = env.get_template("template.html")

    # with open('data_for_html.txt', 'w', encoding='utf-8') as f:
    #     for d in data:
    #         f.write(json.dumps(d))
    #         f.write('\n')
    html_string = template.render(data=data, local=local)

    return html_string


def save_to_html(html_string, dst_path=None):
    """
    Function for saving a file in html format at the specified path

    :param html_string: HTML in string format
    :param dst_path: path to save html file

    """
    if not dst_path:
        dst_path = path.abspath(path.dirname(__file__))
    file_name = path.join(dst_path, str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")) + '.html')
    with open(file_name, 'w',
              encoding='utf-8') as f:
        f.write(html_string)

    return file_name


def save_to_pdf(data, dst_path=None, local=False):
    """
    Function for saving a file in pdf format at the specified path

    :param local: Flag for getting image local or from internet
    :param data: list of articles in dict format
    :param dst_path: path to save pdf file

    """

    if not dst_path:
        dst_path = path.abspath(path.dirname(__file__))

    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.add_font("Sans", style="",
                 fname=path.join(path.abspath(path.dirname(__file__)), 'templates', "NotoSans-Regular.ttf"))
    pdf.add_font("Sans", style="B",
                 fname=path.join(path.abspath(path.dirname(__file__)), 'templates', "NotoSans-Bold.ttf"))
    pdf.add_font("Sans", style="I",
                 fname=path.join(path.abspath(path.dirname(__file__)), 'templates', "NotoSans-Italic.ttf"))
    pdf.add_font("Sans", style="BI",
                 fname=path.join(path.abspath(path.dirname(__file__)), 'templates', "NotoSans-BoldItalic.ttf"))

    pdf.set_font('Sans', size=12)
    pdf.set_auto_page_break(auto=True)
    bar = Bar('Processing generate pdf', max=len(data))

    for d in data:  # Add data to PDF document

        pdf.set_font('Sans', style='B', size=12)
        pdf.write(5, txt='Feed: ' + d.get('Feed', 'No feed'))
        pdf.ln(10)
        pdf.write(5, txt='Title: ' + d.get('Title', 'No Title'))
        pdf.ln(10)
        pdf.set_font('Sans', style='', size=10)
        desc = d.get('Description') if d.get('Description') else 'No description'
        pdf.write(5, txt='Description: ' + desc)
        pdf.ln(5)
        pdf.set_font('Sans', style='I', size=8)
        pdf.write(5, txt='Date: ' + d.get('Date', 'No date'))
        pdf.ln(5)
        link = d.get('Link')
        if link:
            pdf.write_html(f'<p>Article link :<a href="{link}">{link}</a></p>')
        pdf.ln(5)

        media_link = path.join(path.abspath(path.dirname(__file__)), 'templates', 'NoImage.jpg')

        if local:
            media_link = d.get('LocalImgLink')

        else:
            if d.get('Media'):
                media_link = d.get('Media')

        pdf.image(media_link, w=70, type="", link=media_link)
        pdf.ln(5)
        pdf.write_html(f'<p>Image link :<a href="{media_link}">{d.get("Media")}</a></p>')

        pdf.ln(20)
        bar.next()
    bar.finish()
    file_name = path.join(dst_path, str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")) + '.pdf')
    pdf.output(file_name)

    return file_name
