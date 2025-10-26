import os
from TestMaker.maker import make_quiz

# Overall function to make the test pdf file
def make_test(name, questions, keep_tex=False):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "output")

    if not (os.path.exists(output_dir) and os.path.isdir(output_dir)):
        os.mkdir(output_dir)
    else:
        for file in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, file))

    make_quiz(name, questions)
    os.system(f"pdflatex -interaction=nonstopmode -output-directory={output_dir} '{os.path.join(output_dir, f"{name}.tex")}'")

    pdf_bytes = open(os.path.join(output_dir, f"{name}.pdf"), "rb").read()
    if keep_tex:
        tex_bytes = open(os.path.join(output_dir, f"{name}.tex"), "rb").read()

    return pdf_bytes if not keep_tex else (pdf_bytes, tex_bytes)