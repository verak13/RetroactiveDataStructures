from partially_retroactive_queue import PartiallyRetroactiveQueue
from partially_retroactive_priority_queue import PartiallyRetroactivePriorityQueue

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

    print("PARTIALLY RETROACTIVE PRIORITY QUEUE:")
    prpq = PartiallyRetroactivePriorityQueue()

    prpq.add_insert(10, 2)
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.add_insert(20, 6)
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.add_insert(30, 4)
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.add_insert(40, 10)
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.add_delete_min(29)
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.add_delete_min(28)
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.add_insert(15, 1)
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.add_insert(16, -1)
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.remove(28)
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    prpq.remove(30)
    print("Min value: " + str(prpq.get_min()))
    print(prpq)

    print("NOW")
    print(prpq._queue_now)
    print("INSERTS")
    print(prpq._inserts)
    print("DELETED")
    print(prpq._deleted_inserts)
    print("BRIDGES")
    print(prpq._bridges)
