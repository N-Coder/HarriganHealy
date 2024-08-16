from ogdf_python import *

def drawLevelGraph(GA, emb, scaleX=50, scaleY=50):
    maxlvl = max(map(len, emb))
    for y, lvl in enumerate(emb):
        offs = (maxlvl - len(lvl)) * scaleX / 2
        for x, n in enumerate(lvl):
            GA.x[n] = x * scaleX + offs
            GA.y[n] = y * scaleY

def to_cluster(G, LVL):
    CG = ogdf.ClusterGraph(G)
    for ns in LVL.cells():
        c = CG.newCluster(CG.rootCluster())
        for n in ns:
            CG.reassignNode(n, c)
    return CG

def to_cluster_attrs(GA, LVL):
    CG = to_cluster(GA.constGraph(), LVL)
    CGA = ogdf.ClusterGraphAttributes(CG, GA.attributes())
    ogdf.GraphAttributes.__assign__(CGA, GA)
    return CG, CGA

def from_cluster(CG, LVL):
    assert CG.rootCluster().nodes.empty()
    for i, c in enumerate(CG.rootCluster().children):
        assert c.children.empty()
        if i >= LVL.size():
            LVL.newCell()
        for n in c.nodes:
            LVL.moveToCell(n, i)

class MatplotlibLevelGraphEditor(MatplotlibGraphEditor):
    def __init__(self, GA, LVL, *args, dist=100, **kwargs):
        self.LVL = LVL
        self.dist = dist
        for l, ns in enumerate(LVL.cells()):
            for n in ns:
                GA.y[n] = l*dist
        super().__init__(GA, *args, **kwargs)
        for l in range(LVL.size()):
            self.ax.axhline(l * dist, color="lightgray")

    def update_lvl(self, n):
        l = max(0, round(self.GA.y[n] / self.dist))
        while l >= self.LVL.size():
            self.ax.axhline(self.LVL.size() * self.dist, color="lightgray")
            self.LVL.newCell()
        self.GA.y[n] = l * self.dist
        if self.LVL.cellOf(n) != l:
            self.LVL.moveToCell(n, l)

    def update_pos(self, n):
        l = self.LVL.cellOf(n)
        pos = len(self.LVL.cell(l)) - 1
        seen = False
        for i, o in enumerate(self.LVL.cell(l)):
            if self.GA.x[o] > self.GA.x[n]:
                pos = i-1 if seen else i
                break
            elif o == n:
                seen = True
        if self.LVL.positionOf(n) != pos:
            self.LVL.moveToPos(n, pos)
                
    def on_node_moved(self, n):
        self.update_lvl(n)
        self.update_pos(n)
        l = self.LVL.cellOf(n)
        for adj in n.adjEntries:
            e = adj.theEdge()
            self.GA.bends[e].clear()
            if self.LVL.cellOf(adj.twinNode()) == l:
                g.bendEdge(self.GA, e, ((((e.index() * 7) % 10) / 50) + 0.2) * ((e.index() % 2) * 2 - 1))

    def add_node(self, n, *args, **kwargs):
        self.on_node_moved(n)
        super().add_node(n, *args, **kwargs)
