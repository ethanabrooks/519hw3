// Operations
var full = slate.operation("move", {
  "x" : "screenOriginX",
  "y" : "screenOriginY",
  "width" : "screenSizeX",
  "height" : "screenSizeY"
});
var left = full.dup({ "width" : "screenSizeX/2" });
var mid = left.dup({ "x" : "screenOriginX+screenSizeX/3" });
var right = left.dup({ "x" : "screenOriginX+(screenSizeX*1/2)" });
var up = full.dup({ "height" : "screenSizeY/2" });
var down = up.dup({ "y" : "screenOriginY+(screenSizeY*1/2)", });
var leftTop = left.dup({ "height" : "screenSizeY/2" });
var leftBot = leftTop.dup({ "y" : "screenOriginY+screenSizeY/2" });
var midTop = mid.dup({ "height" : "screenSizeY/2" });
var midBot = midTop.dup({ "y" : "screenOriginY+screenSizeY/2" });
var rightTop = right.dup({ "height" : "screenSizeY/2" });
var rightBot = rightTop.dup({ "y" : "screenOriginY+screenSizeY/2" });

var vim_focus = slate.operation("focus", { "app" : "MacVim" });
var chrome_focus = vim_focus.dup({ "app" : "Google Chrome" });
var iterm_focus = vim_focus.dup({ "app" : "iTerm" });
var safari_focus = vim_focus.dup({ "app" : "Safari" });
var skim_focus = vim_focus.dup({ "app" : "Skim" });
var spotify_focus = vim_focus.dup({ "app" : "Spotify" });
var pycharm_focus = vim_focus.dup({ "app" : "PyCharm" });

var relaunch = slate.operation("relaunch");

var right_hash = {
  "operations" : [right]
}

var left_hash = {
  "operations" : [left]
}

var leftBot_hash = {
  "operations" : [leftBot]
}

var leftTop_hash = {
  "operations" : [leftTop]
}

var topBot_hash = {
  "operations" : [leftTop, leftBot]
}

var chrome_vim_layout = slate.layout("chrome_vim_layout", {
  "_after_" : { "operations" : [chrome_focus, vim_focus] },
  "MacVim" : right_hash,
  "Google Chrome" : left_hash
})

var iterm_vim_layout = slate.lay("iterm_vim_layout", {
  "_after_" : { "operations" : [iterm_focus, vim_focus] },
  "MacVim" : right_hash,
  "iTerm" : left_hash
})

var skim_vim_layout = slate.lay("skim_vim_layout", {
  "_after_" : { "operations" : [skim_focus, skim_focus, vim_focus] },
  "MacVim" : right_hash,
  "Skim" : left_hash
})

var latex_layout = slate.lay("latex_layout", {
  "_after_" : { "operations" : [skim_focus, vim_focus] },
  "MacVim" : right_hash,
  "Skim" : topBot_hash
})

var chrome_iterm_layout = slate.lay("chrome_iterm_layout", {
  "_after_" : { "operations" : [chrome_focus, iterm_focus] },
  "iTerm" : right_hash,
  "Google Chrome" : left_hash
})

var run_lay = slate.operation("layout", { "name" : chrome_vim_layout })

var chrome_vim = function() { run_lay.run() }
var iterm_vim = function() { run_lay.dup({ "name" : iterm_vim_layout }).run() }
var skim_vim = function() { run_lay.dup({ "name" : skim_vim_layout }).run() }
var chrome_iterm = function() { run_lay.dup({ "name" : chrome_iterm_layout }).run() }
var latex = function() { run_lay.dup({ "name" : latex_layout }).run() }

// Bindings
slate.bnda({
  "space:alt" : full,
  "h:cmd,alt" : left,
  "l:cmd,alt" : right,
  "u:cmd,alt" : leftTop,
  "i:cmd,alt" : rightTop,
  "m:cmd,alt" : leftBot,
  ",:cmd,alt" : rightBot,

  "c:cmd,alt" : iterm_focus,
  "v:cmd,alt" : vim_focus,
  "b:cmd,alt" : chrome_focus,
  "n:cmd,alt" : safari_focus,
  "s:cmd,alt" : skim_focus,
  "m:cmd,alt" : spotify_focus,
  "p:cmd,alt" : pycharm_focus,

  "0:cmd,alt" : chrome_vim,
  "9:cmd,alt" : iterm_vim,
  "8:cmd,alt" : skim_vim,
  "7:cmd,alt" : chrome_iterm,
  "6:cmd,alt" : latex,

  "[:ctrl" : relaunch
  // "2:cmd,alt" : rightBot,
  // "3:cmd,alt" : rightBot,
})
