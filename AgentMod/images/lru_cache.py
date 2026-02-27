"""
LRU缓存实现
使用哈希表 + 双向链表实现O(1)时间复杂度的get和put操作
"""

class Node:
    """双向链表节点"""
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """LRU缓存类"""
    
    def __init__(self, capacity: int):
        """
        初始化LRU缓存
        :param capacity: 缓存容量
        """
        self.capacity = capacity
        self.cache = {}  # 哈希表：key -> Node
        
        # 使用虚拟头尾节点简化边界处理
        self.head = Node()  # 虚拟头节点
        self.tail = Node()  # 虚拟尾节点
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove_node(self, node: Node):
        """从链表中移除节点"""
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_to_head(self, node: Node):
        """将节点添加到链表头部（表示最近使用）"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def _move_to_head(self, node: Node):
        """将节点移动到链表头部"""
        self._remove_node(node)
        self._add_to_head(node)
    
    def _remove_tail(self) -> Node:
        """移除链表尾部节点（最久未使用）"""
        node = self.tail.prev
        self._remove_node(node)
        return node
    
    def get(self, key: int) -> int:
        """
        获取缓存中的值
        :param key: 键
        :return: 值，如果不存在返回-1
        """
        if key not in self.cache:
            return -1
        
        # 获取节点并移动到头部（标记为最近使用）
        node = self.cache[key]
        self._move_to_head(node)
        return node.value
    
    def put(self, key: int, value: int) -> None:
        """
        向缓存中插入或更新键值对
        :param key: 键
        :param value: 值
        """
        if key in self.cache:
            # key已存在，更新值并移动到头部
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # key不存在，创建新节点
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
            
            # 如果超过容量，移除最久未使用的节点
            if len(self.cache) > self.capacity:
                tail_node = self._remove_tail()
                del self.cache[tail_node.key]
    
    def get_cache_state(self) -> dict:
        """
        获取当前缓存状态（用于调试）
        :return: 按访问顺序排列的键值对字典
        """
        result = {}
        current = self.head.next
        while current != self.tail:
            result[current.key] = current.value
            current = current.next
        return result


# 测试代码
if __name__ == "__main__":
    print("=== LRU缓存测试 ===\n")
    
    # 示例测试
    print("示例测试：")
    lru = LRUCache(2)
    print(f"LRUCache(2): 初始化容量为2的缓存 {lru.get_cache_state()}")
    
    lru.put(1, 1)
    print(f"put(1, 1): 缓存是 {lru.get_cache_state()}")
    
    lru.put(2, 2)
    print(f"put(2, 2): 缓存是 {lru.get_cache_state()}")
    
    result = lru.get(1)
    print(f"get(1): 返回 {result}, 缓存是 {lru.get_cache_state()}")
    
    lru.put(3, 3)
    print(f"put(3, 3): 容量已满，删除最近最少使用的2。缓存变为 {lru.get_cache_state()}")
    
    result = lru.get(2)
    print(f"get(2): 返回 {result} (2已被删除)")
    
    lru.put(4, 4)
    print(f"put(4, 4): 容量已满，删除最近最少使用的1。缓存变为 {lru.get_cache_state()}")
    
    result = lru.get(1)
    print(f"get(1): 返回 {result} (1已被删除)")
    
    result = lru.get(3)
    print(f"get(3): 返回 {result}, 缓存是 {lru.get_cache_state()}")
    
    result = lru.get(4)
    print(f"get(4): 返回 {result}, 缓存是 {lru.get_cache_state()}")
    
    print("\n=== 额外测试 ===\n")
    
    # 测试更新已存在的key
    print("测试更新已存在的key：")
    lru2 = LRUCache(2)
    lru2.put(1, 1)
    lru2.put(2, 2)
    print(f"初始缓存: {lru2.get_cache_state()}")
    lru2.put(1, 10)  # 更新key=1的值
    print(f"put(1, 10)后: {lru2.get_cache_state()}")
    lru2.put(3, 3)   # 应该删除key=2
    print(f"put(3, 3)后: {lru2.get_cache_state()}")
    
    print("\n=== 时间复杂度分析 ===\n")
    print("get操作: O(1)")
    print("  - 哈希表查找: O(1)")
    print("  - 链表节点移动: O(1)")
    print("\nput操作: O(1)")
    print("  - 哈希表查找/插入: O(1)")
    print("  - 链表节点插入/删除: O(1)")
    print("\n空间复杂度: O(capacity)")
    print("  - 哈希表存储: O(capacity)")
    print("  - 双向链表存储: O(capacity)")