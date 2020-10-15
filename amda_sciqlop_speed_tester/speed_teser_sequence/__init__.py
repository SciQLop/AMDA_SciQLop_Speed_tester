from PyQt5.QtCore import Qt, QThread, pyqtSignal
import traceback
from amda_sciqlop_speed_tester.network_probes import trace_route
from amda_sciqlop_speed_tester.simple_downloads import download
from amda_sciqlop_speed_tester.time_measurement import exec_time


def download_probe(url: str):
    result, start, stop = exec_time(download, url)
    return {
        "url": url,
        "data_len": len(result),
        "duration_ns": stop - start
    }


SEQUENCE = {
    "traceroute_google": ("Traceroute google.com", trace_route, "google.com"),
    "traceroute_hephaistos": (
        "Traceroute hephaistos.lpp.polytechnique.fr", trace_route, "hephaistos.lpp.polytechnique.fr"),
    "traceroute_sciqlop": (
        "Traceroute sciqlop.lpp.polytechnique.fr", trace_route, "sciqlop.lpp.polytechnique.fr"),
    "traceroute_amda": ("Traceroute amda.irap.omp.eu", trace_route, "amda.irap.omp.eu"),
    "simple_dl_hephaistos": ("Simple download on hephaistos.lpp.polytechnique.fr", download_probe,
                             "https://hephaistos.lpp.polytechnique.fr/data/jeandet/C1_CP_AUX_ECLAT_FLT_T96__20010101_000000_20141231_235959_V140217.cdf"),
    "simple_dl_sciqlop": ("Simple download on sciqlop.lpp.polytechnique.fr", download_probe,
                          "http://sciqlop.lpp.polytechnique.fr/data/C1_CP_AUX_ECLAT_FLT_T96__20010101_000000_20141231_235959_V140217.cdf"),
    "simple_dl_amda": ("Simple download on amda.cdpp.eu", download_probe,
                       "http://amda.irap.omp.eu/C1_CP_AUX_ECLAT_FLT_T96__20010101_000000_20141231_235959_V140217.cdf"),
    "simple_dl_solo": ("Simple download on solarorbiter.irap.omp.eu", download_probe,
                       "http://solarorbiter.irap.omp.eu/documents/C1_CP_AUX_ECLAT_FLT_T96__20010101_000000_20141231_235959_V140217.cdf")
}

ITEMS = SEQUENCE.keys()
SEQUENCE_HTML = "\n".join(
    ["<li>{{{name}}} {desc}</li>".format(name=key, desc=value[0]) for key, value in SEQUENCE.items()])
_SEQUENCE_HTML = """
    <li>{traceroute} Traceroute</li>
    <li>{sciqlop_rest} Perform some requests on SciQlop cache</li>
    <li>{amda_rest} Perform some requests on AMDA REST API</li>
    <li>{direct_dl} Try several direct files downloads</li>
"""


class TestSequence(QThread):
    message = pyqtSignal(str)
    update_progress = pyqtSignal(str, str)
    push_result = pyqtSignal(dict)
    done = pyqtSignal(bool)

    def run(self):
        result = {}
        for name, task in SEQUENCE.items():
            self.message.emit(f"Doing {name}")
            self.update_progress.emit(name, "pending")
            try:
                result[name] = {"status": "success", "data": task[1](*task[2:])}
                self.message.emit(f"{name} done")
                self.update_progress.emit(name, "done")
            except:
                self.update_progress.emit(name, "failed")
                result[name] = {"status": "failed", "data": traceback.format_exc()}
        self.message.emit("Full test complete")
        self.done.emit(True)
        self.push_result.emit(result)
