import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Cities must match those in CSV
uttarakhand_cities = sorted([
    "Dehradun", "Haridwar", "Rishikesh", "Mussoorie", "Nainital", "Haldwani",
    "Rudrapur", "Kashipur", "Roorkee", "Almora", "Pithoragarh", "Chamoli",
    "Tehri", "Uttarkashi", "Joshimath", "Bageshwar", "Doiwala", "Kichha",
    "Sitarganj", "Khatima", "Tanakpur", "Lohaghat", "Ranikhet", "Kotdwara", "New Tehri"
])

root = tk.Tk()
root.title("Route Rover – Shortest Path Finder")
root.geometry("650x500")

source_var = tk.StringVar()
dest_var = tk.StringVar()

tk.Label(root, text="Source:", font=("Arial", 12)).pack(pady=5)
ttk.Combobox(root, textvariable=source_var, values=uttarakhand_cities, state="readonly").pack(pady=5)

tk.Label(root, text="Destination:", font=("Arial", 12)).pack(pady=5)
ttk.Combobox(root, textvariable=dest_var, values=uttarakhand_cities, state="readonly").pack(pady=5)

output_label = tk.Label(root, text="", font=("Arial", 11), wraplength=600, justify="left")
output_label.pack(pady=20)
def find_route():
    source = source_var.get()
    dest = dest_var.get()

    if not source or not dest:
        messagebox.showwarning("Missing Input", "Please select both cities.")
        return
    if source == dest:
        messagebox.showwarning("Invalid Input", "Source and destination must be different.")
        return

    with open("input.txt", "w", encoding="utf-8") as f:
        f.write(f"{source}\n{dest}\n")

    try:
        subprocess.run(["graph.exe"], check=True)
    except Exception as e:
        output_label.config(text=f" Error running C++: {e}")
        return

    try:
        with open("output.txt", "r", encoding="utf-8") as f:
            result = f.read()
            output_label.config(text=result)
    except:
        output_label.config(text=" Could not read output.txt")
        returnpath = []
    for line in result.splitlines():
        if line.startswith("Path:"):
            path = [p.strip() for p in line.replace("Path:", "").strip().split("→")]

    if not path:
        return

    # Load graph
    df = pd.read_csv("uttarakhand_road_graph.csv")
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_edge(row['from_name'], row['to_name'], weight=row['distance_km'])

    # Plot
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=8)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), font_size=6)

    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange', node_size=700)

    plt.title("Shortest Path Route")
    plt.show()

tk.Button(root, text="Find Route", command=find_route,
          font=("Arial", 12), bg="lightgreen").pack(pady=10)

root.mainloop()