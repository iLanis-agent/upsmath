var UpsMath = (function () {
  function num(x) { return typeof x === "number" && isFinite(x); }
  function pos(x) { return num(x) && x > 0; }
  function r1(x) { return Math.round(x * 10) / 10; }
  function jsnum(x) { if (typeof x === "number" && isFinite(x) && x === Math.trunc(x)) return String(Math.trunc(x)); return String(x); }
  function comma(x) { return String(x).replace(/\B(?=(\d{3})+(?!\d))/g, ","); }
  var PF = 0.6;
  function wattPlan(va) {
    if (!pos(va)) return { error: "the VA rating must be above zero" };
    return { watts: r1(va * PF) };
  }
  function renderWatt(r, va) {
    return "The " + comma(va) + " VA sticker honestly means about " + comma(r.watts)
      + " watts - the box prints volt-amps big and the 0.6 power factor that deflates them small.";
  }
  function runtimePlan(halfWatts, halfMinutes, loadWatts) {
    if (!pos(halfWatts)) return { error: "the half-load watts must be above zero" };
    if (!pos(halfMinutes)) return { error: "the half-load minutes must be above zero" };
    if (!pos(loadWatts)) return { error: "the load must be above zero" };
    var rating = halfWatts * 2;
    var minutes = halfMinutes * halfWatts / loadWatts;
    var verdict = loadWatts > rating ? "it is over the honest rating, and the unit may not hold it at all"
      : loadWatts > halfWatts ? "it is past half load, where the curve bends down"
      : "it sits at or under half load, where inverse minutes stay optimistic";
    return { rating: r1(rating), minutes: r1(minutes), verdict: verdict };
  }
  function renderRuntime(r, halfWatts, halfMinutes, loadWatts) {
    return "The spec sheet's " + jsnum(halfMinutes) + " minutes was measured at " + comma(halfWatts) + " watts; your " + comma(loadWatts)
      + "-watt draw cuts it to about " + jsnum(r.minutes) + " minutes against the " + comma(r.rating) + "-watt honest rating - " + r.verdict + ".";
  }
  function agePlan(minutes, ageYears) {
    if (!pos(minutes)) return { error: "the minutes must be above zero" };
    if (!num(ageYears)) return { error: "the battery age must be a number" };
    if (ageYears < 0) return { error: "the battery age cannot be negative" };
    var factor = Math.max(0.4, 1 - 0.12 * ageYears);
    return { factor: r1(factor * 100), aged: r1(minutes * factor) };
  }
  function renderAge(r, minutes, ageYears) {
    return "At " + jsnum(ageYears) + (ageYears === 1 ? " year" : " years") + " old the lead battery keeps about " + jsnum(r.factor) + "% of its day-one legs - your "
      + jsnum(minutes) + " minutes is honestly " + jsnum(r.aged) + ".";
  }
  return { wattPlan: wattPlan, renderWatt: renderWatt, runtimePlan: runtimePlan, renderRuntime: renderRuntime, agePlan: agePlan, renderAge: renderAge };
})();
if (typeof module !== "undefined" && module.exports) module.exports = UpsMath;
