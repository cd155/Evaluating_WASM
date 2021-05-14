(module
(import "P0lib" "write" (func $write (param i32)))
(import "P0lib" "writeln" (func $writeln))
(import "P0lib" "read" (func $read (result i32)))
(func $fib (param $n i32) (result i32)
(local $r i32)
(local $a i32)
(local $b i32)
(local $0 i32)
local.get $n
i32.const 0
i32.eq
if
i32.const 0
local.set $r
else
local.get $n
i32.const 1
i32.eq
if
i32.const 1
local.set $r
else
local.get $n
i32.const 1
i32.sub
call $fib
local.set $a
local.get $n
i32.const 2
i32.sub
call $fib
local.set $b
local.get $a
local.get $b
i32.add
local.set $r
end
end
local.get $r
)
(global $_memsize (mut i32) i32.const 0)
(func $program
(local $x i32)
(local $0 i32)
call $read
local.set $x
local.get $x
call $fib
local.set $x
local.get $x
call $write
)
(memory 1)
(start $program)
)