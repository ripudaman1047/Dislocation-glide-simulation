
# **Circle-Rolling based Dislocation Line Tension Model**

!["Example"](resources/dislocation_progress.gif)

Circle Rolling is a technique that simulates the glide of a dislocation
through a point-like obstacles distributed on the glide plane. [see Ref-1]

Applications based on various strength distributions of the obstacles are
placed in seperate folders. As input, it takes the number of obsacles, breaking angle (or strength)
of the obstacles, initial normalized shear stress (from 0 to 1), and stress increment size.

The code will output the normalized critically resolved shear stress (CRSS), the area swept
by the dislocation line corresponding the applied normalized shear stress, array of all obstacle coordinates and breaking angle, and the images of the stable configuration of the dislocation line at each stress increment *(can be turned ON or OFF on demand)*.

---

## **REQUIREMENTS**

To use the code, the user should have PYTHON (written with pthon 3.10) along with **[NumPy](https://numpy.org/install/)**, **[SciPy](https://scipy.org/)** and **[Matplotlib](https://matplotlib.org/stable/users/installing/index.html)** libraries installed.

User can also use:

    pip install -r requirements.txt

---

## **USE**

- Open required application folder and launch any preferred terminal in it.
- Type in "main.py" and press enter to run the code.
- Enter the required input as demanded in the prompt.

- To change the image parameters like colors, size, resolution etc., modify the 'visual.py' file.

---

### **REFERENCES**

1) Bharti, Purnima, et al. "Yield strength modeling of an Al-Cu-Li alloy through circle rolling
and flow stress superposition approach." Journal of Alloys and Compounds (2023): 171343. https://doi.org/10.1016/j.jallcom.2023.171343

2) Morris Jr, J. W., & Klahn, D. H. (1974). Thermally activated dislocation glide through a
random array of point obstacles: Computer simulation. Journal of Applied Physics, 45(5), 2027-2038.

---
