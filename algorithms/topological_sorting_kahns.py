class Solution:
# Leetcode Course Schedule
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        adjacency_list = {i:[] for i in range(numCourses)}
        indegree = [0]*numCourses
        topo_queue = []
        for edge in prerequisites:
            adjacency_list[edge[0]].append(edge[1])
            if adjacency_list[edge[0]]:
                indegree[edge[0]] = len(adjacency_list[edge[0]])
            else:
                indegree[edge[0]] = 0
        # indegree,topo_queue = self.refresh(indegree,topo_queue)
        for i,j in enumerate(indegree):
            if j == 0:
                topo_queue.append(i)
        # print(topo_queue,indegree)
        count = 0
        result_queue = []
        while topo_queue:
            for value in topo_queue:
                adjacency_list[value] = [None]
                indegree[value] = None
                for i in adjacency_list:
                    if value in adjacency_list[i]:
                        adjacency_list[i].remove(value)
                        indegree[i] = indegree[i]-1
                result_queue.append(value)
                count += 1
            topo_queue=[]
            # print(topo_queue,indegree)
            for i,j in enumerate(indegree):
                if j == 0:
                    topo_queue.append(i)
                    indegree[i] = None
            # print(topo_queue,indegree)
            # exit(0)
        if count==numCourses:
            return result_queue
        else:
            return []
