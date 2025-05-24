#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <vector>
#include <queue>
#include <limits>
#include <algorithm>
using namespace std;

struct Edge {
    string to;
    double weight;
};

unordered_map<string, vector<Edge>> graph;

void loadGraph(const string& filename) {
    ifstream file(filename);
    if (!file.is_open()) {
        cout << " Could not open file: " << filename << endl;
        return;
    }

    string line;
    getline(file, line); // skip header

    while (getline(file, line)) {
        string from, to, weightStr;
        stringstream ss(line);
        getline(ss, from, ',');
        getline(ss, to, ',');
        getline(ss, weightStr, ',');

        double weight = stod(weightStr);
        graph[from].push_back({to, weight});
        graph[to].push_back({from, weight});
    }
    file.close();
}

unordered_map<string, double> dijkstra(const string& start, unordered_map<string, string>& prev) {
    unordered_map<string, double> dist;
    for (auto& node : graph) {
        dist[node.first] = numeric_limits<double>::infinity();
    }
    dist[start] = 0;

    typedef pair<double, string> P;
    priority_queue<P, vector<P>, greater<P>> pq;
    pq.push(make_pair(0, start));

    while (!pq.empty()) {
        P top = pq.top(); pq.pop();
        double d = top.first;
        string u = top.second;

        if (d > dist[u]) continue;

        for (auto& edge : graph[u]) {
            double alt = dist[u] + edge.weight;
            if (alt < dist[edge.to]) {
                dist[edge.to] = alt;
                prev[edge.to] = u;
                pq.push(make_pair(alt, edge.to));
            }
        }
    }

    return dist;
}

int main() {
    loadGraph("uttarakhand_road_graph.csv");

    ifstream input("input.txt");
    string start, end;
    getline(input, start);
    getline(input, end);
    input.close();

    unordered_map<string, string> prev;
    auto dist = dijkstra(start, prev);

    ofstream output("output.txt", ios::out | ios::binary);
    output << "\xEF\xBB\xBF"; // UTF-8 BOM

    if (dist[end] == numeric_limits<double>::infinity()) {
        output << " No route found between " << start << " and " << end << "\n";
    } else {
        output << " Shortest distance: " << dist[end] << " km\n";
        output << "Path: ";

        vector<string> path;
        string current = end;
        while (prev.find(current) != prev.end()) {
            path.push_back(current);
            current = prev[current];
        }
        path.push_back(current);
        reverse(path.begin(), path.end());

        for (size_t i = 0; i < path.size(); ++i) {
            output << path[i];
            if (i < path.size() - 1) output << " → ";
        }
        output << "\n";
    }

    output.close();
    return 0;
}