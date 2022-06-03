import json
from browser import document, ajax, html, window, timer, console
from wildflower import Downloader

def button_submit(ev):
    timer.set_timeout(start, 0)

def main():
    document["button_submit"].bind("click", button_submit)

    timer.set_timeout(start, 0)

class State:
    pass
gstate = State()

class MyDownloader(Downloader):
    def store(self, url, response):
        pass

    def page_percentage(self, percentage):
        if self != gstate.downloader: return
        document["around"].innerHTML += f"<br>{int(percentage*100)}%"

def start():
    user = document["edit_user"].value
    state = State()
    state.user = user
    gstate.current = state
    document["around"].innerHTML = "loading observations for " + user
    downloader = MyDownloader()
    gstate.downloader = downloader
    downloader.download_pages("https://api.inaturalist.org/v1/observations/species_counts?" +\
            f"user_id={user}", ignore_cache=True, on_success=lambda results: done(results, state))

def done(results, state):
    if state != gstate.current: return
    user = state.user
    obs = {}
    for result in results:
        taxon = result["taxon"]
        obs[taxon["name"]] = taxon["observations_count"], taxon["id"]
    table = html.TABLE()
    document["around"].innerHTML = ""
    document["around"] <= table
    counter = 0
    for ob in sorted(obs.keys(), key=lambda x: obs[x]):
        row = html.TR()
        count, id = obs[ob]
        row <= html.TD(html.A(ob, href=f"https://www.inaturalist.org/observations?taxon_id={id}&user_id={user}"))
        row <= html.TD(str(count))
        table <= row
        counter += 1
        if counter >= 100: break
