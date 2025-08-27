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

    net = Network(notebook=False, height="100%", width="100%", directed=True, 
                  cdn_resources='in_line', bgcolor='#222222', font_color='white')
    
    # Disable the UI buttons that require Bootstrap and cause CORS issues
    net.show_buttons(False)

    net.set_options('''
    var options = {
        "nodes": {
            "size": 15,
            "color": {
                "background": "#ff8c00",
                "border": "#ffa500",
                "highlight": {
                    "background": "#ffae42",
                    "border": "#ffc966"
                }
            },
            "font": {
                "color": "#ffffff",
                "size": 12
            }
        },
        "edges": {
            "arrows": { "to": { "enabled": true, "scaleFactor": 0.5 } },
            "color": { "inherit": false, "color": "#555555", "highlight": "#cccccc" },
            "smooth": { "enabled": true, "type": "dynamic" }
        },
        "physics": {
            "enabled": true,
            "barnesHut": {
                "gravitationalConstant": -8000,
                "centralGravity": 0.3,
                "springLength": 95,
                "springConstant": 0.04,
                "damping": 0.09,
                "avoidOverlap": 0.2
            },
            "maxVelocity": 50,
            "minVelocity": 0.1,
            "solver": "barnesHut"
        },
        "interaction": {
            "hover": true
        }
    }
    ''')

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

        # Reverted the problematic setting, but kept JavascriptEnabled
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
