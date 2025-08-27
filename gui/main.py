import sys
import json
import os
from pyvis.network import Network
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl

def load_graph_data(cache_file):
    """Loads graph data from the JSON cache file."""
    try:
        with open(cache_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {"nodes": [], "edges": []}

def create_interactive_graph_html(graph_data, cache_file):
    """Generates the interactive graph HTML file using pyvis."""
    if not graph_data or not graph_data.get('nodes'):
        return None

    # Reverted to the version that displayed the graph, even with styling issues
    net = Network(notebook=False, height="100%", width="100%", directed=True, 
                  cdn_resources='in_line', bgcolor='#222222', font_color='white')
    
    net.set_options('''var options = {
    "nodes": {
        "size": 8,
        "color": {
            "background": "#7c3aed",
            "border": "#8b5cf6",
            "highlight": {
                "background": "#a855f7",
                "border": "#c084fc"
            }
        },
        "font": {
            "color": "#ffffff",
            "size": 10,
            "face": "Inter, system-ui, sans-serif"
        },
        "borderWidth": 1,
        "shape": "dot"
    },
    "edges": {
        "arrows": { 
            "to": { 
                "enabled": false
            } 
        },
        "color": { 
            "inherit": false, 
            "color": "rgba(255, 255, 255, 0.2)", 
            "highlight": "rgba(124, 58, 237, 0.8)",
            "hover": "rgba(124, 58, 237, 0.6)"
        },
        "smooth": { 
            "enabled": true, 
            "type": "continuous",
            "forceDirection": "none",
            "roundness": 0
        },
        "width": 1,
        "selectionWidth": 2
    },
    "physics": {
        "enabled": true,
        "barnesHut": {
            "gravitationalConstant": -2000,
            "centralGravity": 0.05,
            "springLength": 100,
            "springConstant": 0.04,
            "damping": 0.05,
            "avoidOverlap": 0.15
        },
        "maxVelocity": 30,
        "minVelocity": 0.1,
        "solver": "barnesHut",
        "timestep": 0.35,
        "adaptiveTimestep": true
    },
    "interaction": {
        "hover": true,
        "hoverConnectedEdges": true,
        "selectConnectedEdges": false,
        "tooltipDelay": 200,
        "zoomView": true,
        "dragView": true,
        "dragNodes": true,
        "multiselect": true,
        "keyboard": {
            "enabled": true,
            "bindToWindow": false
        }
    },
    "layout": {
        "randomSeed": 2,
        "improvedLayout": true,
        "hierarchical": {
            "enabled": false
        }
    }
}''')

    for node in graph_data.get('nodes', []):
        net.add_node(node['id'], label=node['label'], title=node['path'])

    for edge in graph_data.get('edges', []):
        net.add_edge(edge['from'], edge['to'])

    html_path = os.path.join(os.path.dirname(cache_file), 'neographnotes_graph.html')
    net.save_graph(html_path)
    return html_path

class GraphWindow(QMainWindow):
    def __init__(self, html_content, base_url):
        super().__init__()
        self.setWindowTitle('NeoGraphNotes')
        self.setGeometry(100, 100, 1024, 768)

        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        if html_content:
            self.browser.setHtml(html_content, base_url)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    cache_file = sys.argv[1]
    app = QApplication(sys.argv)

    graph_data = load_graph_data(cache_file)
    html_path = create_interactive_graph_html(graph_data, cache_file)

    if html_path:
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            base_url = QUrl.fromLocalFile(os.path.dirname(os.path.abspath(html_path)) + os.path.sep)
            
            window = GraphWindow(html_content, base_url)
            window.show()
            sys.exit(app.exec_())

        except FileNotFoundError:
            sys.exit(1)
    else:
        sys.exit(1)