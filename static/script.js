// Tabs
function openCommand(evt, command) {
  var i, tabcontent, tablinks;

  tabcontent = document.getElementsByClassName("tabcontent");

  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  tablinks = document.getElementsByClassName("tablinks");

  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  document.getElementById(command).style.display = "block";
  evt.currentTarget.className += " active";
}


// Used to emphasize and dramatize the actions taken by each computer component
const myCPU = document.getElementById('computer-components-cpu-change-color');
const originalCPUColor = myCPU.style.backgroundColor;

document.addEventListener('click', function(event) {
  if (event.target.classList.contains('lightGreenCPU')) {
    myCPU.style.backgroundColor = 'lightgreen';

    setTimeout(function() {
      myCPU.style.backgroundColor = originalCPUColor;
    }, 10000)
  }  
});


const myRAM = document.getElementById('computer-components-ram-change-color');
const originalRAMColor = myRAM.style.backgroundColor;

document.addEventListener('click', function(event) {
  if (event.target.classList.contains('lightGreenRAM')) {
    myRAM.style.backgroundColor = '#b2d3c2';

    setTimeout(function() {
      myRAM.style.backgroundColor = originalRAMColor;
    }, 10000)
  }  
});


// Change the cache div to a lightgreen background when the cache is needed
const cacheDiv = document.getElementById('computer-components-cpu-inner-cache');
const myCache = document.getElementById('lightGreenCache');
const originalCacheColor = cacheDiv.style.backgroundColor;

// Add a click event listener to the button
myCache.addEventListener('click', function() {
  // Change the background color of the div
  cacheDiv.style.backgroundColor = 'lightgreen';

  setTimeout(function() {
    cacheDiv.style.backgroundColor = originalCacheColor;
  }, 10000)

});


// Change the SSD div to ligthgreen when progress is saved
const ssdDiv = document.getElementById('computer-components-ssd-change-color');
const mySSD = document.getElementById('lightGreenSSD');
const originalSSDColor = ssdDiv.style.backgroundColor;

// Add a click event listener to the button
mySSD.addEventListener('click', function() {
  // Change the background color of the div
  ssdDiv.style.backgroundColor = 'lightgreen';

  // After 2 seconds, revert the background color to the original
  setTimeout(function() {
    ssdDiv.style.backgroundColor = originalSSDColor;
  }, 10000); // 2000 milliseconds = 2 seconds
});