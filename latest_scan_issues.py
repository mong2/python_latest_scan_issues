#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread
from Queue import Queue
import dateutil.parser
import time
from lib.filter import FilteredServer
from lib.servers_controller import ServersController
from lib.scan_controller import ScansController
from lib.issue_controller import IssuesController
from lib.files_controller import FilesController
from lib.log_controller import LogController

MODULE_MAP = {
                "sca": "csm",
                "svm": "sva",
                "fim": "fim"
            }

queue = Queue()
out_queue = Queue()
START_TIME = time.time()
log = LogController()


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
                log.write_log("Successfully retreive %s scan from: %s/%s" % (scans_mod, srv["id"], scans_mod))
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
                log.write_log("Successfully archive %s scan from: %s" % (scan["scan"]["module"], srv["id"]))
                self.files.as_json("%s/server_info" % (filepath), srv)
                log.write_log("Successfully writeout server data for %s" % srv["id"])
            self.out_queue.task_done()


def main():
    print "Start archiving issues."
    log.write_log("start archiving issues.")

    srvs = FilteredServer().aggregated_srvs()

    print "--- %s servers ---" % (len(srvs))
    log.write_log("--- %s servers ---" % (len(srvs)))

    for p in range(3):
        producer = LatestScanIssueProducerThread(queue, out_queue)
        producer.daemon = True
        producer.start()

    for srv in srvs:
        for scans_mod, issues_mod in MODULE_MAP.iteritems():
            queue.put((srv, scans_mod, issues_mod))

    for w in range(2):
        consumer = LatestScanIssueConsumerThread(out_queue)
        consumer.daemon = True
        consumer.start()

    queue.join()
    out_queue.join()

if __name__ == "__main__":
    main()
    print "--- %s seconds ---" % (time.time() - START_TIME)
    log.write_log("--- %s seconds ---" % (time.time() - START_TIME))
