// Google Earth Engine Code Editor script: monthly mean HYCOM surface currents, Sep 2019 to Aug 2024.
// Exported as three int8 GeoTIFFs (four months each), codes of 0.015 m/s, land = -128, last band = water mask.
var c = ee.ImageCollection('HYCOM/sea_water_velocity').filterDate('2019-09-01', '2024-09-01')
  .filter(ee.Filter.calendarRange(0, 0, 'hour')).select(['velocity_u_0', 'velocity_v_0']);
var water = c.mean().select(0).mask().rename('water').unmask(0);
[[1, 4], [5, 8], [9, 12]].forEach(function (r) {
  var bands = [];
  for (var m = r[0]; m <= r[1]; m++) {
    var mm = c.filter(ee.Filter.calendarRange(m, m, 'month')).mean().divide(15).round().clamp(-127, 127);
    bands.push(mm.select('velocity_u_0').rename('u' + m));
    bands.push(mm.select('velocity_v_0').rename('v' + m));
  }
  var out = ee.Image.cat(bands).unmask(-128).addBands(water).toInt8();
  Export.image.toDrive({image: out, description: 'hycom_i8_m' + r[0], folder: 'day13', fileNamePrefix: 'hycom_i8_m' + r[0],
    crs: 'EPSG:4326', crsTransform: [0.25, 0, -180, 0, -0.25, 80], dimensions: '1440x632', maxPixels: 1e10});
});
