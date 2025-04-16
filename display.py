import json
import networkx as nx
import matplotlib.pyplot as plt
import os

def display_tree_single():
    # 讀取 minimax 樹的 JSON 文件
    with open('minimax_tree.json', 'r') as file:
        tree = json.load(file)

    # 創建 NetworkX 的有向圖
    graph = nx.DiGraph()

    # 添加虛擬根節點
    virtual_root = "root"
    graph.add_node(virtual_root, label="Root")

    # 遞迴函數來添加節點和邊
    def add_nodes_and_edges(tree, parent=None, path=""):
        for node, data in tree.items():
            # 為每個節點生成唯一 ID
            unique_id = f"{path}/{node}" if path else node
            # 添加節點
            label = f"{node}\nScore: {data['score']}"
            graph.add_node(unique_id, label=label)
            # 如果有父節點，添加邊
            if parent:
                graph.add_edge(parent, unique_id)
            else:
                # 如果沒有父節點，將其連接到虛擬根節點
                graph.add_edge(virtual_root, unique_id)
            # 遞迴處理子節點
            if 'children' in data and data['children']:
                add_nodes_and_edges(data['children'], unique_id, path=unique_id)

    # 從根節點構建樹
    add_nodes_and_edges(tree)

    # 自定義分層佈局（垂直排列，增加間距）
    def hierarchical_layout(graph, root=None, width=2.0, vert_gap=0.5, xcenter=0.5, pos=None, parent=None, level=0):
        if pos is None:
            pos = {}
        if root is None:
            # 找到圖的根節點（入度為 0 的節點）
            root = [n for n, d in graph.in_degree() if d == 0][0]
        # 設置當前節點的位置
        pos[root] = (xcenter, -level * vert_gap)
        children = list(graph.successors(root))
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = hierarchical_layout(graph, root=child, width=width * 0.8, vert_gap=vert_gap, xcenter=nextx, pos=pos, parent=root, level=level + 1)
        return pos

    # 計算節點位置
    pos = hierarchical_layout(graph)

    # 獲取節點標籤
    labels = nx.get_node_attributes(graph, 'label')

    # 繪製樹
    os.makedirs("plots", exist_ok=True)
    plt.figure(figsize=(20, 12))  # 增加圖形大小
    nx.draw(graph, pos, with_labels=True, labels=labels, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold", arrowsize=15)
    plt.title("Minimax Tree (Vertical Layout)")
    plt.savefig("plots/minimax_tree_single.png")  # 保存為 PNG 文件
    plt.close()
    print("Minimax tree has been saved as 'plots/minimax_tree_single.png'.")

    return 0

def display_tree_separate():
    # 讀取 minimax 樹的 JSON 文件
    with open('minimax_tree.json', 'r') as file:
        tree = json.load(file)

    # 遍歷每個深度 0 的節點，生成子樹
    for root_node, root_data in tree.items():
        # 創建 NetworkX 的有向圖
        graph = nx.DiGraph()

        # 遞迴函數來添加節點和邊
        def add_nodes_and_edges(tree, parent=None, path=""):
            for node, data in tree.items():
                # 為每個節點生成唯一 ID
                unique_id = f"{path}/{node}" if path else node
                # 添加節點
                label = f"{node}\nScore: {data['score']}"
                graph.add_node(unique_id, label=label)
                # 如果有父節點，添加邊
                if parent:
                    graph.add_edge(parent, unique_id)
                # 遞迴處理子節點
                if 'children' in data and data['children']:
                    add_nodes_and_edges(data['children'], unique_id, path=unique_id)

        # 從當前根節點構建子樹
        add_nodes_and_edges({root_node: root_data})

        # 自定義分層佈局（垂直排列，增加間距）
        def hierarchical_layout(graph, root=None, width=2.0, vert_gap=0.5, xcenter=0.5, pos=None, parent=None, level=0):
            if pos is None:
                pos = {}
            if root is None:
                # 找到圖的根節點（入度為 0 的節點）
                root = [n for n, d in graph.in_degree() if d == 0][0]
            # 設置當前節點的位置
            pos[root] = (xcenter, -level * vert_gap)
            children = list(graph.successors(root))
            if len(children) != 0:
                dx = width / len(children)
                nextx = xcenter - width / 2 - dx / 2
                for child in children:
                    nextx += dx
                    pos = hierarchical_layout(graph, root=child, width=width * 0.8, vert_gap=vert_gap, xcenter=nextx, pos=pos, parent=root, level=level + 1)
            return pos

        # 計算節點位置
        pos = hierarchical_layout(graph)

        # 獲取節點標籤
        labels = nx.get_node_attributes(graph, 'label')

        # 繪製子樹
        os.makedirs("plots", exist_ok=True)
        plt.figure(figsize=(20, 12))  # 增加圖形大小
        nx.draw(graph, pos, with_labels=True, labels=labels, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold", arrowsize=15)
        plt.title(f"Subtree for {root_node} (Vertical Layout)")
        plt.savefig(f"plots/minimax_tree_{root_node}.png")  # 保存為 PNG 文件
        plt.close()
        print(f"Subtree for {root_node} has been saved as 'plots/minimax_tree_{root_node}.png'.")

    return 0


if __name__ == '__main__':
    display_tree_single()
    display_tree_separate()