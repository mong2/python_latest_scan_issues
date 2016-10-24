#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread
from Queue import Queue
import dateutil.parser
from lib.servers_controller import ServersController
from lib.scan_controller import ScansController
from lib.issue_controller import IssuesController
from lib.files_controller import FilesController

MODULE_MAP = {
                "sca": "csm",
                "svm": "sva",
                "fim": "fim"
            }

queue = Queue()
out_queue = Queue()

class LatestScanIssueProducerThread(Thread):
    def __init__(self, queue, out_queue):
        Thread.__init__(self)
        self.queue = queue
        self.out_queue = out_queue
        self.servers = ServersController()
        self.issues = IssuesController()
        self.scans = ScansController()

    def run(self):
        while True:
            srv, scans_mod, issues_mod = self.queue.get()
            scan_data = self.servers.show("%s/%s" % (srv["id"], scans_mod))
            if "scan" not in scan_data:
                pass
            elif not scan_data["scan"]["findings"]:
                pass
            else:
                issue_data = self.issues.index(agent_id=srv["id"], issue_type=issues_mod)
                self.out_queue.put([[srv, self.scans.insert_age(scan_data, self.issues.insert_age(issue_data))]])
            self.queue.task_done()

class LatestScanIssueConsumerThread(Thread):
    def __init__(self, out_queue):
        Thread.__init__(self)
        self.out_queue = out_queue
        self.files = FilesController()

    def run(self):
        while True:
            data = self.out_queue.get()
            for srv, scan in data:
                date = dateutil.parser.parse(scan["scan"]["completed_at"])
                filepath = "data/%s/%s/%s/%s" % (date.year, date.month, date.day, srv["id"])
                self.files.as_json("%s/%s_%s" % (filepath, scan["id"], scan["scan"]["module"]), scan)
                self.files.as_json("%s/server_info" % (filepath), srv)
            self.out_queue.task_done()

def main():
    servers = ServersController()
    srvs = servers.index()["servers"]

    for p in range(8):
        producer = LatestScanIssueProducerThread(queue, out_queue)
        producer.daemon = True
        producer.start()

    for srv in srvs:
        for scans_mod, issues_mod in MODULE_MAP.iteritems():
            queue.put((srv, scans_mod, issues_mod))

    for w in range(5):
        consumer = LatestScanIssueConsumerThread(out_queue)
        consumer.daemon = True
        consumer.start()

    queue.join()
    out_queue.join()

if __name__ == "__main__":
    main()