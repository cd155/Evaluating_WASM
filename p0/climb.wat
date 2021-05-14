(module
(import "P0lib" "write" (func $write (param i32)))
(import "P0lib" "writeln" (func $writeln))
(import "P0lib" "read" (func $read (result i32)))
(func $plus (param $n i32) (result i32)
(local $a i32)
(local $0 i32)
i32.const 0
local.set $a
loop
local.get $a
local.get $n
i32.lt_s
if
local.get $a
i32.const 1
i32.add
local.set $a
br 1
end
end
local.get $a
)
(global $_memsize (mut i32) i32.const 0)
(func $program
(local $x i32)
(local $0 i32)
call $read
local.set $x
local.get $x
call $plus
local.set $x
local.get $x
call $write
)
(memory 1)
(start $program)
)