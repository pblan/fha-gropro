# generate whole class diagram 
pyreverse -o pdf --ignore=io.py,plotter.py spidercam_simulator && mv *.pdf uml;

# generate class diagram for a single module
for f in spidercam_simulator/*.py; do pyreverse -o pdf $f && mv classes.pdf uml/$(basename $f .py).pdf; done