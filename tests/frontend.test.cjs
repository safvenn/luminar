const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
class Element {
  constructor() { this.value = ''; this.dataset = {}; this.children = []; this.classList = {toggle(){}, add(){}}; }
  setAttribute() {} addEventListener() {} focus() {} scrollIntoView() {}
  replaceChildren(...children) { this.children = children; }
  append(...children) { this.children.push(...children); }
  add(child) { this.children.push(child); }
  querySelector() { return null; }
}
const elements = new Map();
const element = id => { if (!elements.has(id)) elements.set(id, new Element()); return elements.get(id); };
const context = vm.createContext({
  document: {getElementById: element, documentElement: {dataset: {}}, querySelector: () => new Element(), querySelectorAll: () => [], createElement: () => new Element(), createElementNS: () => new Element()},
  localStorage: {setItem(){}}, Option: function(text,value) {this.text=text;this.value=value;},
  AbortController, setTimeout, clearTimeout, requestAnimationFrame: fn => fn(), matchMedia: () => ({matches:true}),
  fetch: async () => ({ok:true,json:async () => ({train_no:'16346',report_id:'test',prediction_available:true,data:[
    {station_code:'ERS',station_name:'Ernakulam',current_route:true,prediction_available:true,scheduled_arrival:'13:10:00',scheduled_departure:'13:15:00',distance_km:206,previous_distance_diff:33,station_time_difference:54,arrival_day_offset:0,departure_day_offset:0},
    {station_code:'LTT',current_route:true,prediction_available:true,scheduled_arrival:'17:05:00',arrival_day_offset:1},
    {station_code:'VVH',current_route:false,prediction_available:false,scheduled_arrival:'16:00:00',schedule_source:'training_history',prediction_reason:'Historical station entry'}
  ]})})
});
vm.runInContext(fs.readFileSync('frontend/app.js','utf8'),context);
(async () => {
  await vm.runInContext("loadTrain('16346', '2026-11-02')",context);
  assert.equal(element('station').children.length,4);
  assert.equal(vm.runInContext("canSelectStation('LTT')",context),true);
  assert.equal(vm.runInContext("canSelectStation('VVH')",context),false);
  assert.equal(vm.runInContext("estimatedArrival('23:50:00',20,null,0)",context),'12:10 AM · Day 2');
  assert.equal(vm.runInContext("estimatedArrival('17:05:00',0,null,1)",context),'5:05 PM · Day 2');
  assert.ok(element('route-stations').children[0].children.some(x => x.textContent === '206 km from origin'));
  vm.runInContext('resetJourney()',context);
  assert.equal(vm.runInContext("canSelectStation('LTT')",context),false);
  console.log('Frontend: distant stop selection, historical display, distances, day rollover, journey reset passed.');
})().catch(error => {console.error(error);process.exitCode=1;});
