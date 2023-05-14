from simple_retroactive_data_structures.partially_retroactive_queue import PartiallyRetroactiveQueue
from simple_retroactive_data_structures.partially_retroactive_stack import PartiallyRetroactiveStack
from partially_retroactive_priority_queue.partially_retroactive_priority_queue import PartiallyRetroactivePriorityQueue

if __name__ == '__main__':

    print("PARTIALLY RETROACTIVE QUEUE:")
    prq = PartiallyRetroactiveQueue()
    prq.insert_enqueue(value=2, time=10)
    print(prq)
    prq.insert_enqueue(value=4, time=20)
    print(prq)
    prq.insert_enqueue(value=6, time=30)
    print(prq)
    prq.insert_enqueue(value=10)
    print(prq)
    prq.insert_dequeue(time=28)
    print(prq)
    prq.insert_enqueue(value=8, time=15)
    print(prq)
    prq.insert_dequeue(time=16)
    print(prq)
    prq.delete_operation(time=40)
    print(prq)
    prq.delete_operation(time=28)
    print(prq)
    dequeue_operation = prq.insert_dequeue()
    print("First value: " + str(dequeue_operation.node))
    print(prq)

    print("------------------------------------------------------------------------------")

    print("PARTIALLY RETROACTIVE STACK:")
    prs = PartiallyRetroactiveStack()
    prs.insert_push(2, 10)
    print(prs)
    prs.insert_push(4, 20)
    print(prs)
    prs.insert_push(6, 30)
    print(prs)
    prs.insert_pop(28)
    print(prs)
    prs.insert_push(8, 15)
    print(prs)
    prs.insert_pop(16)
    print(prs)
    prs.delete_operation(30)
    print(prs)
    prs.delete_operation(28)
    print(prs)
    pop_operation = prs.insert_pop()
    print("Popped value: " + str(pop_operation.node))
    print(prs)

    print("------------------------------------------------------------------------------")

    print("PARTIALLY RETROACTIVE PRIORITY QUEUE:")
    prpq = PartiallyRetroactivePriorityQueue()

    prpq.add_insert(10, 2, "2")
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.add_insert(20, 6, "6")
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.add_insert(30, 4, "4")
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.add_insert(40, 10, "10")
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.add_delete_min(29)
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.add_delete_min(28)
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.add_insert(15, 1, "1")
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.add_insert(16, -1, "-1")
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.remove(28)
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.remove(30)
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    print("LENGTH: " + str(len(prpq)))
    print("NOW")
    print(prpq._queue_now)
    print("INSERTS")
    print(prpq._inserts)
    print("DELETED")
    print(prpq._deleted_inserts)
    print("BRIDGES")
    print(prpq._bridges)