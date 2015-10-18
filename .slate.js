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

var relaunch = slate.operation("relaunch");

var vim_hash = {
    "operations" : [right]
  }

var chrome_hash = {
    "operations" : [left]
  }

var iterm_hash = {
    "operations" : [left]
  }

var chrome_vim_layout = slate.layout("chrome_vim_layout", {
  "_after_" : { "operations" : [chrome_focus, vim_focus] },
  "MacVim" : vim_hash,
  "Google Chrome" : chrome_hash
})

var iterm_vim_layout = slate.lay("iterm_vim_layout", {
  "_after_" : { "operations" : [iterm_focus, vim_focus] },
  "MacVim" : vim_hash,
  "iTerm" : iterm_hash
})

var latex_layout = slate.lay("latex_layout", {
  "MacVim" : [right],
  "Skim" : [leftTop],
  "iTerm" : [leftBot]
})

var run_lay = slate.operation("layout", { "name" : chrome_vim_layout })

var chrome_vim = function() { run_lay.run() }
var iterm_vim = function() { run_lay.dup({ "name" : iterm_vim_layout }).run() }

// Bindings
slate.bnda({
  "space:cmd,alt" : full,
  "h:cmd,alt" : left,
  "j:cmd,alt" : down,
  "k:cmd,alt" : up,
  "l:cmd,alt" : right,
  "u:cmd,alt" : leftTop,
  "i:cmd,alt" : rightTop,
  "m:cmd,alt" : leftBot,
  ",:cmd,alt" : rightBot,

  "c:cmd,alt" : iterm_focus,
  "v:cmd,alt" : vim_focus,
  "b:cmd,alt" : chrome_focus,

  "0:cmd,alt" : chrome_vim,
  "9:cmd,alt" : iterm_vim,

  "[:ctrl" : relaunch
  // "2:cmd,alt" : rightBot,
  // "3:cmd,alt" : rightBot,
})
