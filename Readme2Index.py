import markdown
import sys 

def makeindex(markfile='README.md', outfile=''):
    with open(markfile, 'r') as file:
        md_text = file.read()

    # Simple conversion in memory
    html = markdown.markdown(md_text)

    return html

if __name__ == "__main__":
    html = makeindex(sys.argv[1])
    print(html)
