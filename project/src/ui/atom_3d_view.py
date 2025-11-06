from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel, QFileDialog, QOpenGLWidget, QSizePolicy
from PyQt5.QtCore import Qt
import math
from PyQt5.QtGui import QFont
try:
    import numpy as np  # opcional
    import pyqtgraph as pg
    import pyqtgraph.opengl as gl
    USE_PYQTGRAPH = True
except Exception:
    USE_PYQTGRAPH = False
    np = None  # garantiza que el nombre exista aunque numpy no esté disponible
    # PyOpenGL para fallback sin numpy/pyqtgraph
    from OpenGL.GL import (
        glClearColor, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
        glEnable, GL_DEPTH_TEST, glMatrixMode, GL_PROJECTION, GL_MODELVIEW,
        glLoadIdentity, glTranslatef, glRotatef, glBegin, glEnd, GL_LINES,
        glColor3f, glViewport, glVertex3f, glPushMatrix, glPopMatrix
    )
    from OpenGL.GLU import gluPerspective, gluNewQuadric, gluSphere, gluCylinder


class Atom3DView(QWidget):
    """Vista 3D simple para visualizar moléculas educativas (ej: H2O).

    Usa PyQtGraph GL para renderizar esferas (átomos) y líneas (enlaces).
    Pensado para demostración visual, no para precisión química.
    """

    def __init__(self, parent_view, molecule: str = "H2O"):
        super().__init__()
        self.parent_view = parent_view
        self.view = None
        self.gl_canvas = None
        if USE_PYQTGRAPH:
            self.view = gl.GLViewWidget()
            # Fondo verde suave para diferenciar de blanco/negro/gris
            self.view.setBackgroundColor('#BFD8B8')
            self.view.orbit(35, 20)
            self.view.setCameraPosition(distance=20)
        else:
            class SimpleGLCanvas(QOpenGLWidget):
                def __init__(self, parent=None):
                    super().__init__(parent)
                    self.atoms = []  # [(element, (x,y,z))]
                    self.bonds = []  # [(i,j)]
                    self.distance = 20.0
                    self.azimuth = 35.0
                    self.elevation = 20.0
                    self._quadric = None
                    self.setMouseTracking(True)
                    self._last_pos = None

                def set_scene(self, atoms, bonds):
                    self.atoms = atoms
                    self.bonds = bonds
                    self.update()

                def initializeGL(self):
                    # Fondo verde suave en fallback OpenGL
                    glClearColor(0.75, 0.85, 0.72, 1.0)
                    glEnable(GL_DEPTH_TEST)
                    self._quadric = gluNewQuadric()

                def resizeGL(self, w, h):
                    glViewport(0, 0, w, h if h > 0 else 1)
                    glMatrixMode(GL_PROJECTION)
                    glLoadIdentity()
                    aspect = w / float(h if h > 0 else 1)
                    gluPerspective(45.0, aspect, 0.1, 100.0)
                    glMatrixMode(GL_MODELVIEW)

                def paintGL(self):
                    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                    glLoadIdentity()
                    glTranslatef(0.0, 0.0, -self.distance)
                    glRotatef(self.elevation, 1.0, 0.0, 0.0)
                    glRotatef(self.azimuth, 0.0, 1.0, 0.0)

                    # Colores por elemento
                    color_map = {
                        'H': (1.0, 1.0, 1.0),
                        'O': (1.0, 0.2, 0.2),
                        'C': (0.2, 0.2, 0.2),
                        'N': (0.2, 0.2, 1.0),
                    }
                    radius_map = {
                        'H': 0.6,
                        'O': 1.0,
                        'C': 0.9,
                        'N': 0.95,
                    }

                    # Enlaces como cilindros (soporta dobles/triples con cilindros paralelos)
                    for b in self.bonds:
                        try:
                            i = int(b[0]); j = int(b[1])
                            order = int(b[2]) if (isinstance(b, (list, tuple)) and len(b) >= 3) else 1
                        except Exception:
                            continue
                        p1 = self.atoms[i][1]
                        p2 = self.atoms[j][1]
                        # Calcular offset lateral para dobles/triples
                        vx = p2[0] - p1[0]
                        vy = p2[1] - p1[1]
                        vz = p2[2] - p1[2]
                        n = math.sqrt(vx*vx + vy*vy + vz*vz)
                        if n <= 1e-6:
                            continue
                        ux, uy, uz = vx / n, vy / n, vz / n
                        bx, by, bz = 0.0, 0.0, 1.0
                        px = uy*bz - uz*by
                        py = uz*bx - ux*bz
                        pz = ux*by - uy*bx
                        pm = math.sqrt(px*px + py*py + pz*pz)
                        if pm <= 1e-6:
                            bx, by, bz = 0.0, 1.0, 0.0
                            px = uy*bz - uz*by
                            py = uz*bx - ux*bz
                            pz = ux*by - uy*bx
                            pm = math.sqrt(px*px + py*py + pz*pz)
                            if pm <= 1e-6:
                                px, py, pz = 1.0, 0.0, 0.0
                                pm = 1.0
                        px, py, pz = px/pm, py/pm, pz/pm
                        sep = 0.3
                        offsets = [0.0] if order <= 1 else ([sep, -sep] if order == 2 else [0.0, sep, -sep])
                        for s in offsets:
                            ox, oy, oz = px*s, py*s, pz*s
                            q1 = (p1[0]+ox, p1[1]+oy, p1[2]+oz)
                            q2 = (p2[0]+ox, p2[1]+oy, p2[2]+oz)
                            # Dibujar cilindro entre q1 y q2
                            self._draw_cylinder(q1, q2, radius=0.12)

                    # Átomos como esferas (GLU)
                    for el, pos in self.atoms:
                        color = color_map.get(el, (0.7, 0.7, 0.7))
                        r = radius_map.get(el, 0.8)
                        glPushMatrix()
                        glTranslatef(*pos)
                        glColor3f(*color)
                        gluSphere(self._quadric, r, 20, 20)
                        glPopMatrix()

                def _draw_cylinder(self, p1, p2, radius=0.12):
                    # Construye un cilindro GLU alineado con el vector p1->p2
                    vx = p2[0] - p1[0]
                    vy = p2[1] - p1[1]
                    vz = p2[2] - p1[2]
                    length = math.sqrt(vx*vx + vy*vy + vz*vz)
                    if length <= 1e-6:
                        return
                    ux, uy, uz = vx / length, vy / length, vz / length
                    # Ángulo entre eje Z y dirección del cilindro
                    dot = max(-1.0, min(1.0, (0.0*ux + 0.0*uy + 1.0*uz)))
                    angle = math.degrees(math.acos(dot))
                    # Eje de rotación: z x u
                    rx = 0.0*uz - 1.0*uy
                    ry = 1.0*ux - 0.0*uz
                    rz = 0.0*uy - 0.0*ux
                    norm = math.sqrt(rx*rx + ry*ry + rz*rz)
                    if norm <= 1e-6:
                        rx, ry, rz = 1.0, 0.0, 0.0
                    else:
                        rx, ry, rz = rx/norm, ry/norm, rz/norm
                    glPushMatrix()
                    glTranslatef(p1[0], p1[1], p1[2])
                    if angle > 1e-3:
                        glRotatef(angle, rx, ry, rz)
                    glColor3f(0.6, 0.6, 0.6)
                    gluCylinder(self._quadric, radius, radius, length, 20, 1)
                    glPopMatrix()

                def mousePressEvent(self, ev):
                    self._last_pos = (ev.x(), ev.y())

                def mouseMoveEvent(self, ev):
                    if self._last_pos is None:
                        return
                    dx = ev.x() - self._last_pos[0]
                    dy = ev.y() - self._last_pos[1]
                    self.azimuth += dx * 0.3
                    self.elevation += dy * 0.3
                    self._last_pos = (ev.x(), ev.y())
                    self.update()

                def wheelEvent(self, ev):
                    delta = ev.angleDelta().y() / 120.0
                    self.distance = max(5.0, min(60.0, self.distance - delta * 2.0))
                    self.update()

            self.gl_canvas = SimpleGLCanvas()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Top bar con navegación y controles (altura fija, márgenes reducidos)
        top_bar = QWidget()
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(16, 10, 16, 6)
        top_layout.setSpacing(8)

        back_btn = QPushButton("← Volver")
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(
            "padding: 8px 16px; border-radius: 8px; background-color: #4CAF50; color: white; border: none;"
        )
        back_btn.clicked.connect(self._go_back)

        controls_container = QWidget()
        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(8)
        mol_label = QLabel("Molécula:")
        mol_label.setStyleSheet("color: #333;")
        self.mol_combo = QComboBox()
        self.mol_combo.addItems(["H2O", "CO2", "CH4", "NH3", "O2", "N2", "CO", "Etanol", "Benceno", "NaCl", "Metano Clorado", "Etileno", "Acetileno", "Glucosa"])
        self.mol_combo.setCurrentText(molecule)
        self.mol_combo.currentTextChanged.connect(self.load_molecule)

        # (El selector de modo de enlaces fue removido; siempre se usan cilindros)

        # Botón para re-centrar y resetear cámara
        reset_btn = QPushButton("Reset vista")
        reset_btn.setCursor(Qt.PointingHandCursor)
        reset_btn.setStyleSheet(
            "padding: 6px 12px; border-radius: 8px; background-color: #9E9E9E; color: white; border: none;"
        )
        reset_btn.clicked.connect(lambda: self.load_molecule(self.mol_combo.currentText()))

        load_json_btn = QPushButton("Cargar JSON…")
        load_json_btn.setCursor(Qt.PointingHandCursor)
        load_json_btn.setStyleSheet(
            "padding: 6px 12px; border-radius: 8px; background-color: #2196F3; color: white; border: none;"
        )
        load_json_btn.clicked.connect(self._choose_json_file)

        controls_layout.addWidget(mol_label)
        controls_layout.addWidget(self.mol_combo)
        controls_layout.addWidget(load_json_btn)
        # Espaciado eliminado junto con el selector de enlaces
        controls_layout.addWidget(reset_btn)
        controls_container.setLayout(controls_layout)

        top_layout.addWidget(back_btn, alignment=Qt.AlignLeft)
        top_layout.addStretch()
        top_layout.addWidget(controls_container, alignment=Qt.AlignRight)
        top_bar.setLayout(top_layout)
        top_bar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        top_bar.setFixedHeight(56)

        layout.addWidget(top_bar)
        layout.addWidget(self.view or self.gl_canvas)
        # Asegura que el visor 3D tome el espacio disponible
        layout.setStretch(0, 0)
        layout.setStretch(1, 1)
        if self.view is not None:
            self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if self.gl_canvas is not None:
            self.gl_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setLayout(layout)

        if USE_PYQTGRAPH:
            self._axes()
        self.load_molecule(molecule)

    def _axes(self):
        # Ejes XYZ para referencia
        axis = gl.GLAxisItem()
        axis.setSize(5, 5, 5)
        self.view.addItem(axis)

    def _go_back(self):
        try:
            self.parent_view.return_to_module()
        except Exception:
            pass

    def _choose_json_file(self):
        try:
            path, _ = QFileDialog.getOpenFileName(self, "Selecciona archivo JSON", "", "JSON (*.json)")
            if path:
                self.load_from_json(path)
        except Exception:
            pass

    def load_molecule(self, molecule: str):
        # Limpieza previa
        if USE_PYQTGRAPH:
            for item in list(self.view.items):
                if not isinstance(item, gl.GLAxisItem):
                    self.view.removeItem(item)

        # Parámetros simples de visualización
        colors = {
            'H': (1.0, 1.0, 1.0, 1),  # blanco
            'O': (1.0, 0.2, 0.2, 1),  # rojo
            'C': (0.2, 0.2, 0.2, 1),  # gris oscuro
            'N': (0.2, 0.2, 1.0, 1),  # azul
            'Na': (0.4, 0.6, 1.0, 1), # celeste
            'Cl': (0.0, 0.6, 0.0, 1), # verde
        }
        radii = {
            'H': 0.6,
            'O': 1.0,
            'C': 0.9,
            'N': 0.95,
            'Na': 1.2,
            'Cl': 1.6,
        }

        def _vec(x: float, y: float, z: float):
            # Utiliza numpy si está disponible, de lo contrario listas nativas
            return np.array([x, y, z]) if (np is not None) else [x, y, z]

        # Definiciones sencillas de moléculas
        atoms = []
        bonds = []

        if molecule.upper() == 'H2O':
            # Geometría aproximada (no exacta): ángulo ~104.5°
            atoms = [
                ('O', _vec(0.0, 0.0, 0.0)),
                ('H', _vec(1.5, 1.0, 0.0)),
                ('H', _vec(-1.5, 1.0, 0.0)),
            ]
            bonds = [(0, 1), (0, 2)]
        elif molecule.upper() == 'CO2':
            atoms = [
                ('O', _vec(-2.0, 0.0, 0.0)),
                ('C', _vec(0.0, 0.0, 0.0)),
                ('O', _vec(2.0, 0.0, 0.0)),
            ]
            bonds = [(0, 1), (1, 2)]
        elif molecule.upper() == 'CH4':
            # Tetraédrica aproximada
            atoms = [
                ('C', _vec(0.0, 0.0, 0.0)),
                ('H', _vec(1.5, 1.5, 1.5)),
                ('H', _vec(-1.5, -1.5, 1.5)),
                ('H', _vec(-1.5, 1.5, -1.5)),
                ('H', _vec(1.5, -1.5, -1.5)),
            ]
            bonds = [(0, 1), (0, 2), (0, 3), (0, 4)]
        elif molecule.upper() == 'NH3':
            # Piramidal trigonal aproximada
            atoms = [
                ('N', _vec(0.0, 0.5, 0.0)),
                ('H', _vec(1.5, -0.5, 0.0)),
                ('H', _vec(-1.5, -0.5, 0.0)),
                ('H', _vec(0.0, -0.5, 1.5)),
            ]
            bonds = [(0, 1), (0, 2), (0, 3)]
        elif molecule.upper() == 'O2':
            atoms = [
                ('O', _vec(-1.2, 0.0, 0.0)),
                ('O', _vec(1.2, 0.0, 0.0)),
            ]
            bonds = [(0, 1, 2)]
        elif molecule.upper() == 'N2':
            atoms = [
                ('N', _vec(-1.3, 0.0, 0.0)),
                ('N', _vec(1.3, 0.0, 0.0)),
            ]
            bonds = [(0, 1, 3)]
        elif molecule.upper() == 'CO':
            atoms = [
                ('C', _vec(0.0, 0.0, 0.0)),
                ('O', _vec(1.3, 0.0, 0.0)),
            ]
            bonds = [(0, 1, 3)]
        elif molecule.lower() == 'etanol' or molecule.lower() == 'ethanol':
            # Cadena aproximada: C-C-O con hidrógenos alrededor
            atoms = [
                ('C', _vec(0.0, 0.0, 0.0)),
                ('C', _vec(1.5, 0.0, 0.0)),
                ('O', _vec(3.0, 0.2, 0.0)),
                ('H', _vec(-0.9, 0.9, 0.0)),
                ('H', _vec(-0.9, -0.9, 0.0)),
                ('H', _vec(0.0, 0.0, 1.1)),
                ('H', _vec(1.5, 1.0, 0.9)),
                ('H', _vec(1.5, -1.0, -0.9)),
                ('H', _vec(3.8, 0.9, 0.0)),
            ]
            bonds = [(0,1),(1,2),(0,3),(0,4),(0,5),(1,6),(1,7),(2,8)]
        elif molecule.lower() == 'benceno' or molecule.lower() == 'benzene':
            # Anillo hexagonal plano con H externos
            r_c = 2.0
            r_h = 3.0
            atoms = []
            for i in range(6):
                ang = math.radians(60 * i)
                cx = r_c * math.cos(ang)
                cy = r_c * math.sin(ang)
                atoms.append(('C', _vec(cx, cy, 0.0)))
            for i in range(6):
                ang = math.radians(60 * i)
                hx = r_h * math.cos(ang)
                hy = r_h * math.sin(ang)
                atoms.append(('H', _vec(hx, hy, 0.0)))
            bonds = []
            for i in range(6):
                order = 2 if (i % 2 == 0) else 1  # alterna dobles/simples
                bonds.append((i, (i+1) % 6, order))  # C-C en anillo
                bonds.append((i, 6 + i))            # C-H
        elif molecule.upper() == 'NACL':
            # Par iónico simple Na-Cl
            atoms = [
                ('Na', _vec(-1.5, 0.0, 0.0)),
                ('Cl', _vec(1.5, 0.0, 0.0)),
            ]
            bonds = [(0, 1)]
        elif molecule.lower() == 'metano clorado':
            # CH3Cl tetraédrico aproximado (Cl más separado)
            atoms = [
                ('C', _vec(0.0, 0.0, 0.0)),
                ('Cl', _vec(2.4, 0.0, 0.0)),
                ('H', _vec(-1.5, -1.5, 1.5)),
                ('H', _vec(-1.5, 1.5, -1.5)),
                ('H', _vec(1.5, -1.5, -1.5)),
            ]
            bonds = [(0,1),(0,2),(0,3),(0,4)]
        elif molecule.lower() == 'etileno' or molecule.lower() == 'ethylene':
            # C2H4 plano aproximado
            atoms = [
                ('C', _vec(-1.2, 0.0, 0.0)),
                ('C', _vec(1.2, 0.0, 0.0)),
                ('H', _vec(-1.2, 1.0, 0.0)),
                ('H', _vec(-1.2, -1.0, 0.0)),
                ('H', _vec(1.2, 1.0, 0.0)),
                ('H', _vec(1.2, -1.0, 0.0)),
            ]
            bonds = [(0,1,2),(0,2),(0,3),(1,4),(1,5)]
        elif molecule.lower() == 'acetileno' or molecule.lower() == 'acetylene':
            # C2H2 lineal
            atoms = [
                ('C', _vec(-1.5, 0.0, 0.0)),
                ('C', _vec(1.5, 0.0, 0.0)),
                ('H', _vec(-2.6, 0.0, 0.0)),
                ('H', _vec(2.6, 0.0, 0.0)),
            ]
            bonds = [(0,1,3),(0,2),(1,3)]
        elif molecule.lower() == 'glucosa' or molecule.lower() == 'glucose':
            # Representación simplificada: anillo de 6 carbonos con 6 OH y 6 H
            rc = 2.0
            ro = 3.0
            atoms = []
            c_idx = []
            o_idx = []
            ho_idx = []
            hc_idx = []
            for i in range(6):
                ang = math.radians(60 * i)
                cx = rc * math.cos(ang)
                cy = rc * math.sin(ang)
                c_idx.append(len(atoms))
                atoms.append(('C', _vec(cx, cy, 0.0)))
                # Oxígeno externo
                ox = ro * math.cos(ang)
                oy = ro * math.sin(ang)
                o_idx.append(len(atoms))
                atoms.append(('O', _vec(ox, oy, 0.0)))
                # H del OH
                hox = (ro + 0.8) * math.cos(ang)
                hoy = (ro + 0.8) * math.sin(ang)
                ho_idx.append(len(atoms))
                atoms.append(('H', _vec(hox, hoy, 0.0)))
                # H sobre el carbono (ligeramente hacia fuera)
                hcx = (rc + 1.0) * math.cos(ang + math.radians(25))
                hcy = (rc + 1.0) * math.sin(ang + math.radians(25))
                hc_idx.append(len(atoms))
                atoms.append(('H', _vec(hcx, hcy, 0.0)))
            bonds = []
            for i in range(6):
                bonds.append((c_idx[i], c_idx[(i+1) % 6]))  # anillo C-C
                bonds.append((c_idx[i], o_idx[i]))          # C-O
                bonds.append((o_idx[i], ho_idx[i]))         # O-H
                bonds.append((c_idx[i], hc_idx[i]))         # C-H
        else:
            # Por defecto muestra H2O
            atoms = [
                ('O', _vec(0.0, 0.0, 0.0)),
                ('H', _vec(1.5, 1.0, 0.0)),
                ('H', _vec(-1.5, 1.0, 0.0)),
            ]
            bonds = [(0, 1), (0, 2)]

        if USE_PYQTGRAPH:
            # Recentrado simple: calcula centro y tamaño
            if np is not None and len(atoms) > 0:
                pts = np.array([pos for _, pos in atoms])
                center = pts.mean(axis=0)
                atoms = [(el, (pos - center)) for el, pos in atoms]

            # Render con PyQtGraph
            sphere_md = gl.MeshData.sphere(rows=32, cols=32)
            for el, pos in atoms:
                color = colors.get(el, (0.7, 0.7, 0.7, 1))
                radius = radii.get(el, 0.8)
                mesh = gl.GLMeshItem(meshdata=sphere_md, smooth=True, shader='shaded', color=color, glOptions='opaque')
                mesh.scale(radius, radius, radius)
                mesh.translate(*pos)
                self.view.addItem(mesh)

            # Enlaces con soporte de orden
            for b in bonds:
                if isinstance(b, (list, tuple)):
                    i = int(b[0]); j = int(b[1])
                    order = int(b[2]) if len(b) >= 3 else 1
                else:
                    continue
                p1 = atoms[i][1]
                p2 = atoms[j][1]
                # siempre cilindros
                if np is not None:
                    self._add_bond_cylinders(p1, p2, order=order, radius=0.18, color=(0.6, 0.6, 0.6, 1))

            # Auto-zoom basado en tamaño
            if np is not None and len(atoms) > 0:
                pts = np.array([pos for _, pos in atoms])
                max_r = float(np.max(np.linalg.norm(pts, axis=1)))
                self.view.setCameraPosition(distance=max(10.0, max_r * 2.6))
        else:
            # Fallback: enviar escena al canvas OpenGL
            self.gl_canvas.set_scene(atoms, bonds)

    def load_from_json(self, file_path: str):
        import json
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            return

        atoms = []
        bonds = []
        for a in (data.get('atoms') or []):
            el = a.get('element') or 'C'
            pos = [float(a.get('x', 0.0)), float(a.get('y', 0.0)), float(a.get('z', 0.0))]
            atoms.append((el, pos))
        for b in (data.get('bonds') or []):
            if not isinstance(b, (list, tuple)):
                continue
            if len(b) >= 3:
                bonds.append((int(b[0]), int(b[1]), int(b[2])))
            elif len(b) == 2:
                bonds.append((int(b[0]), int(b[1])))

        if USE_PYQTGRAPH:
            for item in list(self.view.items):
                if not isinstance(item, gl.GLAxisItem):
                    self.view.removeItem(item)
            colors = {
                'H': (1.0, 1.0, 1.0, 1),
                'O': (1.0, 0.2, 0.2, 1),
                'C': (0.2, 0.2, 0.2, 1),
                'N': (0.2, 0.2, 1.0, 1),
            }
            radii = {
                'H': 0.6,
                'O': 1.0,
                'C': 0.9,
                'N': 0.95,
            }
            # Recentrado
            if np is not None and len(atoms) > 0:
                pts = np.array([pos for _, pos in atoms])
                center = pts.mean(axis=0)
                atoms = [(el, (np.array(pos) - center)) for el, pos in atoms]

            sphere_md = gl.MeshData.sphere(rows=32, cols=32)
            for el, pos in atoms:
                color = colors.get(el, (0.7, 0.7, 0.7, 1))
                radius = radii.get(el, 0.8)
                mesh = gl.GLMeshItem(meshdata=sphere_md, smooth=True, shader='shaded', color=color, glOptions='opaque')
                mesh.scale(radius, radius, radius)
                mesh.translate(*pos)
                self.view.addItem(mesh)
            for b in bonds:
                if isinstance(b, (list, tuple)):
                    i = int(b[0]); j = int(b[1])
                    order = int(b[2]) if len(b) >= 3 else 1
                else:
                    continue
                p1 = atoms[i][1]
                p2 = atoms[j][1]
                # siempre cilindros
                if np is not None:
                    self._add_bond_cylinders(p1, p2, order=order, radius=0.18, color=(0.6, 0.6, 0.6, 1))

            if np is not None and len(atoms) > 0:
                pts = np.array([pos for _, pos in atoms])
                max_r = float(np.max(np.linalg.norm(pts, axis=1)))
                self.view.setCameraPosition(distance=max(10.0, max_r * 2.6))

    # Helpers -----------------------------
    def _add_cylinder(self, p1, p2, radius=0.2, color=(0.6, 0.6, 0.6, 1)):
        if not USE_PYQTGRAPH or np is None:
            return
        v = np.array(p2) - np.array(p1)
        length = float(np.linalg.norm(v))
        if length <= 1e-6:
            return
        u = v / length
        z = np.array([0.0, 0.0, 1.0])
        dot = float(np.clip(np.dot(z, u), -1.0, 1.0))
        angle = float(np.degrees(np.arccos(dot)))
        axis = np.cross(z, u)
        # Mesh cilíndrico de longitud exacta alineado con Z
        cyl_md = gl.MeshData.cylinder(rows=12, cols=24, radius=[radius, radius], length=length)
        mesh = gl.GLMeshItem(meshdata=cyl_md, smooth=True, shader='shaded', color=color, glOptions='opaque')
        if angle > 1e-3:
            if np.linalg.norm(axis) < 1e-6:
                axis = np.array([1.0, 0.0, 0.0])
            mesh.rotate(angle, axis[0], axis[1], axis[2])
        # Posiciona desde p1 (cilindro va de z=0 a z=length)
        mesh.translate(*p1)
        self.view.addItem(mesh)

    def _add_bond_cylinders(self, p1, p2, order=1, radius=0.18, color=(0.6, 0.6, 0.6, 1)):
        # Renderiza enlaces múltiples con cilindros paralelos
        if order <= 1:
            self._add_cylinder(p1, p2, radius=radius, color=color)
            return
        if np is None:
            return
        v = np.array(p2) - np.array(p1)
        n = float(np.linalg.norm(v))
        if n <= 1e-6:
            return
        u = v / n
        base = np.array([0.0, 0.0, 1.0])
        perp = np.cross(u, base)
        if float(np.linalg.norm(perp)) < 1e-6:
            base = np.array([0.0, 1.0, 0.0])
            perp = np.cross(u, base)
        perp = perp / float(np.linalg.norm(perp))
        sep = 0.3
        if order == 2:
            off = perp * sep
            self._add_cylinder(np.array(p1) + off, np.array(p2) + off, radius=radius*0.95, color=color)
            self._add_cylinder(np.array(p1) - off, np.array(p2) - off, radius=radius*0.95, color=color)
        else:
            off = perp * sep
            self._add_cylinder(np.array(p1), np.array(p2), radius=radius*0.9, color=color)
            self._add_cylinder(np.array(p1) + off, np.array(p2) + off, radius=radius*0.9, color=color)
            self._add_cylinder(np.array(p1) - off, np.array(p2) - off, radius=radius*0.9, color=color)