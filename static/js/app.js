// Minimal JS: nav toggle and basic accessibility behaviors
document.addEventListener('DOMContentLoaded', function(){
  var btn = document.getElementById('nav-toggle');
  var nav = document.getElementById('primary-nav');
  if(btn && nav){
    btn.addEventListener('click', function(){
      var expanded = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!expanded));
      if(!expanded){
        nav.style.display = 'block';
      } else {
        nav.style.display = 'none';
      }
    });
  }

  // Plan invest form validation and confirmation modal
  var investForm = document.querySelector('form[action="/invest"]');
  if(investForm){
    var input = investForm.querySelector('input[name="local_amount"]');
    var errorBox = document.getElementById('local_amount_error');
    var modal = document.getElementById('confirmModal');
    var confirmBody = document.getElementById('confirmBody');
    var confirmOk = document.getElementById('confirmOk');
    var confirmCancel = document.getElementById('confirmCancel');
    investForm.addEventListener('submit', function(e){
      e.preventDefault();
      var val = parseFloat(input.value || '0');
      var minLocal = parseFloat(input.getAttribute('data-min-local')) || 0;
      var maxLocal = parseFloat(input.getAttribute('data-max-local')) || null;
      var rate = parseFloat(input.getAttribute('data-rate')) || 0;
      var symbol = input.getAttribute('data-currency-symbol') || '';
      // enforce min
      if(minLocal && val < minLocal){
        if(errorBox){ errorBox.style.display='block'; errorBox.textContent = 'Minimum amount is ' + symbol + minLocal.toFixed(2); }
        return;
      }
      // enforce max if present
      if(maxLocal && val > maxLocal){
        if(errorBox){ errorBox.style.display='block'; errorBox.textContent = 'Maximum amount is ' + symbol + maxLocal.toFixed(2); }
        return;
      }
      if(errorBox){ errorBox.style.display='none'; errorBox.textContent = ''; }
      // compute approx USD using rate if available
      var approxUsd = null;
      if(rate && rate > 0){ approxUsd = val / rate; }
      var html = '<p>Local amount: <strong>' + symbol + val.toFixed(2) + '</strong></p>';
      if(approxUsd !== null){ html += '<p>Approx. in USD: <strong>$' + approxUsd.toFixed(2) + '</strong></p>'; }
      else { html += '<p><em>USD conversion unavailable — server will compute accurate value.</em></p>'; }
      html += '<p>Plans are defined in USD; this action will create a pending investment recorded in USD.</p>';
      if(confirmBody) confirmBody.innerHTML = html;
      if(modal) modal.style.display = 'flex';
      // wire confirm
      confirmOk.onclick = function(){
        modal.style.display = 'none';
        investForm.submit();
      };
      confirmCancel.onclick = function(){ modal.style.display = 'none'; };
    });
  }
  // Countdown timers for plan cards
  function pad(n){return n<10?'0'+n:n}
  function formatRemaining(ms){
    if(ms<=0) return '00:00:00';
    var s=Math.floor(ms/1000);
    var days=Math.floor(s/86400); s%=86400;
    var hrs=Math.floor(s/3600); s%=3600;
    var mins=Math.floor(s/60); var secs=s%60;
    if(days>0) return days+'d '+pad(hrs)+':'+pad(mins)+':'+pad(secs);
    return pad(hrs)+':'+pad(mins)+':'+pad(secs);
  }
  var cds = document.querySelectorAll('.countdown[data-end]');
  if(cds.length){
    function tick(){
      var now = new Date();
      cds.forEach(function(el){
        var end = el.getAttribute('data-end');
        var endDate = new Date(end);
        if(isNaN(endDate)){
          // try numeric seconds
          var secs = parseInt(end,10);
          if(!isNaN(secs)) endDate = new Date(Date.now() + secs*1000);
        }
        var rem = endDate - now;
        var span = el.querySelector('.countdown-timer');
        if(rem <= 0){
          span.textContent = 'Offer ended';
        } else {
          span.textContent = formatRemaining(rem);
        }
      });
    }
    tick();
    setInterval(tick,1000);
  }

  // admin dropdown toggle for small screens
  var adminToggle = document.getElementById('admin-toggle');
  var adminMenu = document.getElementById('admin-menu');
  if(adminToggle && adminMenu){
    adminToggle.addEventListener('click', function(e){
      e.preventDefault();
      var open = adminToggle.getAttribute('aria-expanded') === 'true';
      adminToggle.setAttribute('aria-expanded', String(!open));
      adminMenu.style.display = open ? 'none' : 'block';
    });
    // close when clicking outside
    document.addEventListener('click', function(ev){
      if(!adminMenu.contains(ev.target) && ev.target !== adminToggle){
        adminMenu.style.display = 'none';
        adminToggle.setAttribute('aria-expanded','false');
      }
    });
  }
});
