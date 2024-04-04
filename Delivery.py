import re
import sys


class TreeNode:
    def __init__(self, order_id=None, current_system_time=None,
                 order_value=None, delivery_time=None):
        self.order_id = order_id
        self.current_system_time = current_system_time
        self.order_value = order_value
        self.delivery_time = delivery_time
        self.ETA = None

        if current_system_time is not None and order_value is not None:
            self.priority = 0.3 * (order_value / 50) - (0.7 * current_system_time)
        else:
            self.priority = None

        self.left = None
        self.right = None
        self.height = 1



class AVL_Tree(object):
    def __init__(self):
        self.root = None

    def _balance_and_rotate(self, root, node, balance, is_left_child):
        if balance > 1:
            if is_left_child:
                if node.priority < root.left.priority:
                    return self._right_rotate(root)
                else:
                    root.left = self._left_rotate(root.left)
                    return self._right_rotate(root)
            else:
                if node.priority > root.right.priority:
                    return self._left_rotate(root)
                else:
                    root.right = self._right_rotate(root.right)
                    return self._left_rotate(root)
        return root


    def insert(self, root, node):
        if not root:
            return node

        current = root
        while current:
            if node.priority < current.priority:
                if current.left is None:
                    current.left = node
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = node
                    break
                current = current.right

        current = node
        while current:
            current.height = self.calculate_height(current)
            current = self.balance_tree(current, node)

            if current:
                break

        return root

    def calculate_height(self, node):
        if not node:
            return 0
        left_height = 0 if not node.left else node.left.height
        right_height = 0 if not node.right else node.right.height
        return 1 + max(left_height, right_height)

    def balance_tree(self, current, node):
        balance = self.getBalance(current)

        switch = {
            balance > 1 and node.priority < current.left.priority: self.rightRotate,
            balance < -1 and node.priority > current.right.priority: self.leftRotate,
            balance > 1 and node.priority > current.left.priority: lambda x: self.rotate(self.rotate(x.left,"left"),"right"),
            balance < -1 and node.priority < current.right.priority: lambda x: self.rotate(self.rotate(x.right,"right"),"left")
        }

        current = switch.get(True, lambda x: None)(current)
        return current

    def rotate(self, z, direction):
        if direction == "left":
            y = z.right
            T2 = y.left

            y.left = z
            z.right = T2
        elif direction == "right":
            y = z.left
            T3 = y.right

            y.right = z
            z.left = T3

        z_height_left = self.getHeight(z.left)
        z_height_right = self.getHeight(z.right)
        y_height_left = self.getHeight(y.left)
        y_height_right = self.getHeight(y.right)

        if z_height_left > z_height_right:
            z_height = 1 + z_height_left
        else:
            z_height = 1 + z_height_right

        if y_height_left > y_height_right:
            y_height = 1 + y_height_left
        else:
            y_height = 1 + y_height_right

        z.height = z_height
        y.height = y_height

        return y

    def leftRotate(self, z):
        y = z.right
        z.right = y.left
        y.left = z
        
        z_left_height = 0 if z.left is None else z.left.height
        z_right_height = 0 if z.right is None else z.right.height
        y_left_height = 0 if y.left is None else y.left.height
        y_right_height = 0 if y.right is None else y.right.height
        
        if z_left_height > z_right_height:
            z_height = z_left_height
        else:
            z_height = z_right_height
        
        if y_right_height > z_height:
            y.height = y_right_height + 1
        else:
            y.height = z_height + 1
        
        return y


    def rightRotate(self, z):
        y = z.left
        z.left = y.right
        y.right = z
        
        z_left_height = 0 if z.left is None else z.left.height
        z_right_height = 0 if z.right is None else z.right.height
        y_left_height = 0 if y.left is None else y.left.height
        y_right_height = 0 if y.right is None else y.right.height
        
        if z_left_height > z_right_height:
            z_height = z_left_height
        else:
            z_height = z_right_height
        
        if y_left_height > z_height:
            y.height = y_left_height + 1
        else:
            y.height = z_height + 1
        
        return y


    def getHeight(self, root):
        return root.height if root else 0

    def getBalance(self, root):
        return self.getHeight(root.left) - self.getHeight(root.right) if root else 0

    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root

        min_node = root.left
        while min_node.left is not None:
            min_node = min_node.left
        
        return min_node

    def preOrder(self, root, tmp_list=None):
        if tmp_list is None:
            tmp_list = []
        if not root:
            return


        return preOrder2(root, tmp_list)



    def preOrder2(self, root,tmp_list=None):
        result = tmp_list
        if result is None:
            result = []
        stack = []
        current = root

        while stack or current:
            if current:
                result.append(current)
                stack.append(current.right)
                current = current.left
            else:
                current = stack.pop()

        return result
    def inOrder(self, root, tmp_list=None):
        if tmp_list is None:
            tmp_list = []
        if not root:
            return

        return self.inOrder2(root, tmp_list)

    def inOrder2(self, root, tmp_list=None):
        result = tmp_list
        if result is None:
            result = []
        stack = []
        current = root

        while stack or current:
            if current:
                stack.append(current)
                current = current.right
            else:
                current = stack.pop()
                result.append(current)
                current = current.left

        return result


    def get_path(self, root, orderId):
        if root is None:
            a=[]
            return a
        if orderId== root.order_id:
            return [root]

        rp = self.get_path(root.right, orderId)

        lp = self.get_path(root.left, orderId)

        if lp:
            lp.append(root)
            return lp

        elif rp:
            rp.append(root)
            return rp

        return []
    # def x(int n):
    #   return x(n-1)+x(n-2)
    def get_path_iterative(self, root, orderId):
        stack = []
        visited = set()

        while root or stack:
            if root:
                stack.append(root)
                root = root.left
            else:
                node = stack[-1]
                if node.right and node.right not in visited:
                    root = node.right
                else:
                    if node.orderId == orderId:
                        return stack[:]
                    visited.add(node)
                    stack.pop()
                    root = None
        return None

    def get_near_large_node(self, root, orderId):
      path = self.get_path(root, orderId)
      if path[0].right:
          right = path[0].right
          while right.left:
              right = right.left
          return right
      
      i = 0
      while i < len(path):
          if path[i].priority > path[0].priority:
              return path[i]
          i += 1


    def printHelper(self, root):
      if not root:
          return

      stack = [(root, '', True)]
      while stack:
          node, indent, last = stack.pop()
          sys.stdout.write(indent)
          if last:
            prefix = "R----"
            indent += "     "
          else:
            prefix = "L----"
            indent += "|    "

          print(f"{prefix}{node.priority}")

          if node.right:
              stack.append((node.right, indent, True))
          if node.left:
              stack.append((node.left, indent, False))



class Order(TreeNode):
    def __init__(self, order_id=None, current_system_time=None,
                 order_value=None, delivery_time=None):
        super().__init__(order_id=order_id, current_system_time=current_system_time,
                         order_value=order_value, delivery_time=delivery_time)


class OrderManagementSystem(AVL_Tree):
    def __init__(self, current_time=0, order_count=0,
                 delivery_time=0, return_time=0):
        super().__init__()
        self.current_time = current_time
        self.order_count = order_count
        self.delivery_time = delivery_time
        self.return_time = return_time

    def create_order(self, order_id, current_system_time, order_value, delivery_time):
        self.current_time = current_system_time
        self.delivery_time = delivery_time
        del_orders = self.get_delivered()

        fresh_order = self.create_fresh_order(order_id, current_system_time, order_value, delivery_time)
        self.update_first_order_priority(fresh_order)

        self.root = self.insert_order_into_tree(self.root, fresh_order)

        self.calculate_and_update_ETA(fresh_order)

        self.print_order_creation_message(fresh_order)
        self.order_count += 1
        self.check_and_print_order_updates(fresh_order.order_id, del_orders)

    def create_fresh_order(self, order_id, current_system_time, order_value, delivery_time):
        return Order(order_id, current_system_time, order_value, delivery_time)

    def update_first_order_priority(self, fresh_order):
        ord_arr = self.inOrder(self.root)
        if ord_arr:
            first_order = ord_arr[0]
            if (fresh_order.priority > first_order.priority) and \
                    ((first_order.ETA - first_order.delivery_time) <= self.current_time):
                first_order.priority = 100

    def insert_order_into_tree(self, root, fresh_order):
        return self.insert(root, fresh_order)

    def calculate_and_update_ETA(self, fresh_order):
        larger_node = self.get_near_large_node(self.root, fresh_order.order_id)
        if not larger_node:
            if self.return_time < self.current_time:
                fresh_order.ETA = self.current_time + self.delivery_time
            else:
                fresh_order.ETA = self.return_time + self.delivery_time
        else:
            fresh_order.ETA = larger_node.ETA + larger_node.delivery_time + fresh_order.delivery_time

    def print_order_creation_message(self, fresh_order):
        print(f"Order {fresh_order.order_id} has been created - ETA: {fresh_order.ETA}")

    def check_and_print_order_updates(self, order_id, order_delivered):
        self.check_for_order_updates(order_id)
        self.print_delivered(order_delivered)

    def check_for_order_updates(self, order_id):
      order_list = self.inOrder(self.root)
      if order_list is None:
          return

      index = 0
      found = False
      while index < len(order_list):
          order = order_list[index]
          if order.order_id == order_id:
              found = True
              break
          index += 1

      updated_later_orders = []
      next_index = index + 1
      while next_index < len(order_list):
          order_list[next_index].ETA = order_list[next_index - 1].ETA + \
                                      order_list[next_index - 1].delivery_time + \
                                      order_list[next_index].delivery_time
          updated_later_orders.append(order_list[next_index])
          next_index += 1

      if len(updated_later_orders) != 0:
          s = "Updated ETAs: ["
          j = 0
          while j < len(updated_later_orders):
              order = updated_later_orders[j]
              s += str(order.order_id) + ":" + str(order.ETA)
              if j != len(updated_later_orders) - 1:
                  s += ","
              j += 1
          s += "]"
          print(s)


    def cancel_order(self, order_id, current_system_time):
        self.current_time = current_system_time
        order_delivered = self.get_delivered()
        ord_arr = self.inOrder(self.root)
        found, key = self.find_order(order_id, ord_arr)

        if not found:
            print(f"Cannot cancel. Order {order_id} has already been delivered.")
        else:
            order_to_cancel = ord_arr[key]
            if self.is_order_out_for_delivery(order_to_cancel, current_system_time):
                print(f"Cannot cancel. Order {order_id} is out for delivery.")
            else:
                updated_orders = self.update_order_ETAs_after_cancellation(order_to_cancel, ord_arr, key)
                print(f"Order {order_id} has been canceled")
                if updated_orders:
                    self.print_updated_ETAs(updated_orders)
                self.root = self.delete(self.root, order_to_cancel.priority)

        self.print_delivered(order_delivered)

    def find_order(self, order_id, ord_arr):
        for index, order in enumerate(ord_arr):
            if order.order_id == order_id:
                return True, index
        return False, None

    def is_order_out_for_delivery(self, order, current_system_time):
        order_departure_moment = order.ETA - order.delivery_time
        return order_departure_moment < current_system_time

    def update_order_ETAs_after_cancellation(self, order_to_cancel, ord_arr, cancel_index):
        updated_orders = []
        if cancel_index + 1 == len(ord_arr):
            return updated_orders
        elif cancel_index == 0:
            second_order_index = cancel_index + 1
            ord_arr[second_order_index].ETA = self.return_time + ord_arr[second_order_index].delivery_time
            updated_orders.append(ord_arr[second_order_index])
            for i in range(second_order_index + 1, len(ord_arr)):
                ord_arr[i].ETA = ord_arr[i - 1].ETA + ord_arr[i - 1].delivery_time + ord_arr[i].delivery_time
                updated_orders.append(ord_arr[i])
        else:
            ord_arr[cancel_index + 1].ETA = ord_arr[cancel_index - 1].ETA + ord_arr[cancel_index - 1].delivery_time + ord_arr[cancel_index + 1].delivery_time
            updated_orders.append(ord_arr[cancel_index + 1])
            connecting_order_index = cancel_index + 1
            for i in range(connecting_order_index + 1, len(ord_arr)):
                ord_arr[i].ETA = ord_arr[i - 1].ETA + ord_arr[i - 1].delivery_time + ord_arr[i].delivery_time
                updated_orders.append(ord_arr[i])
        return updated_orders

    def print_updated_ETAs(self, updated_orders):
        new_ETA = ", ".join([f"{order.order_id}:{order.ETA}" for order in updated_orders])
        print(f"Updated ETAs: [{new_ETA}]")


    def get_rank_of_order(self, order_id):
      order_list = self.inOrder(self.root)
      if order_list is None:
          return 0

      count = 0
      found = False
      while count < len(order_list):
          order = order_list[count]
          if order.order_id == order_id:
              found = True
              break
          count += 1

      if found:
          print(f"Order {order_id} will be delivered after {count} orders.")
      return count


    def update_time(self, order_id, current_system_time, new_delivery_time):
        found = True
        order_delivered = self.get_delivered()
        order_list = self.inOrder(self.root)
        key = 0
        self.current_time = current_system_time
        found = not found
        for key, order in enumerate(order_list):
            if order.order_id != order_id:
                continue
            else:
                found = True
                break

        if found == False:
            sys.stdout.write(
                f"Cannot update. Order {order_id} has already been delivered.\n")
        else:
            order_departure_moment = order_list[key].ETA - \
                order_list[key].delivery_time
            if order_departure_moment > current_system_time:
                dif = new_delivery_time
                dif -= order_list[key].delivery_time
                order_list[key].ETA += dif
                order_list[key].delivery_time = new_delivery_time
                i = key + 1
                while i < len(order_list):
                    order_list[i].ETA += 2 * dif
                    i += 1
                s = "Updated ETAs: ["
                for key in range(key, len(order_list)):
                    s += str(order_list[key].order_id) + \
                        ":" + str(order_list[key].ETA)
                    if key != len(order_list) - 1:
                        s += ","
                s += "]"
                print(s)
            else:
                print(f"Cannot update. Order {order_id} is out for delivery.")

        self.print_delivered(order_delivered)

    def print_trees(self):
        sys.stdout.write("\n==============================\n")
        sys.stdout.write(">>> Priority Tree:\n")
        self._pre_order(self.root)
        self._in_order(self.root)
        sys.stdout.write("\n")
        self._display_helper(self.root, "", True)
        sys.stdout.write("==============================\n\n")

    def print_within_time(self, **kwargs):
      time1 = kwargs.get("time1")
      time2 = kwargs.get("time2")

      if "order_id" in kwargs:
          node_list = self.get_path(self.root, kwargs["order_id"])
          print(f"[{node_list[0].order_id}, "
                f"{node_list[0].current_system_time}, "
                f"{node_list[0].order_value}, "
                f"{node_list[0].delivery_time}, "
                f"{node_list[0].ETA}]")
          return

      order_list = self.inOrder(self.root)
      if order_list is None:
          print("There are no orders in that time period")
          return

      result = [order for order in order_list if time1 <= order.ETA <= time2]
      if result:
          print(f"[{','.join(str(order.order_id) for order in result)}]")
      else:
          print("There are no orders in that time period")


    def get_delivered(self):
      order_list = self.inOrder(self.root)
      if order_list is None:
          return []
      
      delivered_list = []
      index = 0
      while index < len(order_list) and order_list[index].ETA <= self.current_time:
          delivered_list.append(order_list[index])
          self.return_time = order_list[index].ETA + order_list[index].delivery_time
          self.root = self.delete(self.root, order_list[index].priority)
          index += 1
      
      return delivered_list


    def print_delivered(self, delivered_list=None):
      if delivered_list is None:
          return

      count = 0
      while count < len(delivered_list):
          order = delivered_list[count]
          print(f"Order {order.order_id} has been delivered at time {order.ETA}")
          count += 1


    def quit(self, tmp_list=None):
      tmp_list = tmp_list or []
      self.inOrder(self.root, tmp_list)
      print('\n'.join([f"Order {order.order_id} has been delivered at time {order.ETA}" for order in tmp_list]))


    def delete(self, root, priority):
      if not root:
          return root

      if priority < root.priority:
          root.left = self.delete(root.left, priority)

      elif priority > root.priority:
          root.right = self.delete(root.right, priority)

      else:
          if root.left is None:
              return root.right

          if root.right is None:
              return root.left

          tmp_root = self.getMinValueNode(root.right)
          root.priority = tmp_root.priority
          root.order_id = tmp_root.order_id
          root.current_system_time = tmp_root.current_system_time
          root.order_value = tmp_root.order_value
          root.delivery_time = tmp_root.delivery_time
          root.ETA = tmp_root.ETA
          root.right = self.delete(root.right, tmp_root.priority)

      if root is None:
          return root

      root.height = 1 + max(self.getHeight(root.left),
                            self.getHeight(root.right))

      balance = self.getBalance(root)

      # Switch case approach
      if balance > 1:
          if self.getBalance(root.left) >= 0:
              return self.rotate(root, "right")
          else:
              root.left = self.rotate(root.left, "left")
              return self.rotate(root, "right")

      if balance < -1:
          if self.getBalance(root.right) <= 0:
              return self.rotate(root, "left")
          else:
              root.right = self.rotate(root.right, "right")
              return self.rotate(root, "left")

      return root



def main():
    test_cases = ["TC1","TC2","TC3"]

    for test_case in test_cases:
        output_file_name = test_case.split('/')[-1].replace('input', 'output') + '.txt'
        with open(output_file_name, 'w') as output_file:
            sys.stdout = output_file  # Redirect stdout to the output file

            oms = OrderManagementSystem()

            with open(test_case, 'r') as file:
                lines = file.readlines()
            for line in lines:
                command = line.strip().split('(')
                if command[0] == 'Quit':
                    oms.quit()
                    break
                elif command[0] == 'print':
                    times = command[1].split(',')
                    oms.print_within_time(time1=int(times[0].strip()), time2=int(times[1].strip()[:-1]))
                else:
                    params = command[1][:-1].split(',')
                    if command[0] == 'createOrder':
                        oms.create_order(int(params[0]), int(params[1]), int(params[2]), int(params[3]))
                    elif command[0] == 'getRankOfOrder':
                        oms.get_rank_of_order(int(params[0]))
                    elif command[0] == 'updateTime':
                        oms.update_time(int(params[0]), int(params[1]), int(params[2]))
                    elif command[0] == 'cancelOrder':
                        oms.cancel_order(int(params[0]), int(params[1]))

            sys.stdout = sys.__stdout__  # Reset stdout to console
            print("Test case", test_case, "completed.\n")
            print("---------------------------------------------------")
            print("***************************************************")
            print("---------------------------------------------------")
            print()



if __name__ == "__main__":
    main()

