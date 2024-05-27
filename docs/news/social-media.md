---
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: false

# from https://gitlab.com/idotj/mastodon-embed-timeline
---

# Social Media News

News from Mastodon [#OpenWebCalendar](https://toot.wales/tags/OpenWebCalendar).

<div id="mt-container" class="mt-container">
  <div class="mt-body" role="feed">
    <div class="mt-loading-spinner"></div>
  </div>
</div>

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@idotj/mastodon-embed-timeline@4.4.2/dist/mastodon-timeline.min.css" integrity="sha256-1UGgxsonaMCfOEnVOL89aMKSo3GEAmaRP0ISbsWa6lU=" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/@idotj/mastodon-embed-timeline@4.4.2/dist/mastodon-timeline.umd.js" integrity="sha256-E6WPG6iq+qQIzvu3HPJJxoAeRdum5siq13x4ITjyxu8=" crossorigin="anonymous"></script>

<script type="text/javascript">
  window.addEventListener("load", () => {
    const myTimeline = new MastodonTimeline.Init({
      instanceUrl: "https://toot.wales",
      timelineType: "hashtag",
      hashtagName: "OpenWebCalendar",
    });
  });
</script>
