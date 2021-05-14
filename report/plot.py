
# time from 1-50 fib between each wasm file
# test in safari, Version 14.0.3
# OS: macOS Big Sur 11.2.3 
# CPU: 2.9 GHz Dual-Core Intel Core i5
# time from 1-40 fib between one wasm to Javascript
# 1, 5, 10, 15, 20, 25, 30, 35, 40, 41, 42, 43, 44, 45, 50
# in chrome Version 89.0.4389.114
# unite ms, millisecond

fib_range_1_50 = [1, 5, 10, 15, 20, 25, 30, 35, 40, 41, 42, 43, 44, 45, 50]

fib_as_1_50 = [0.003173828125, 0.004150390625, 0.0029296875, 0.010986328125, 0.0849609375, 
           0.898193359375, 12.91162109375, 121.944091796875, 1399.376953125, 2158.877197265625, 
           3371.23583984375, 5483.010009765625, 8941.166748046875, 14318.2109375, 151937.02490234375]

fib_js_as_1_50 = [0.0048828125, 0.010986328125, 0.01708984375, 0.12890625, 2.239990234375, 
             1.795654296875, 19.0810546875, 172.9931640625, 1786.39111328125, 2850.632080078125, 
             4655.699951171875, 7323.510009765625, 11790.563720703125, 19066.866943359375, 253357.89184570312]

fib_go_1_50 = [0.3408203125, 0.323974609375, 0.151123046875, 0.2109375, 0.527099609375, 
          4.1171875, 45.277099609375, 440.25390625, 4883.194091796875, 7890.422119140625, 
          12691.843017578125, 21574.85693359375, 33360.442138671875, 53604.88720703125, 599487.087890625]

fib_js_go_1_50 = [0.004150390625, 0.00830078125, 0.026123046875, 0.161865234375, 2.326904296875,
             1.96923828125, 18.824951171875, 171.006103515625, 1783.681884765625, 2994.22900390625, 
             4550.93310546875, 7319.653076171875, 11806.609130859375, 19066.376953125, 247948.74096679688]

fib_rust_1_50 = [0.0029296875, 0.00390625, 0.005859375, 0.01611328125, 0.1689453125, 
            1.22314453125, 13.85009765625, 122.482177734375, 1232.61767578125, 1955.02099609375, 
            3134.13134765625, 5036.819091796875, 8093.65478515625, 13097.222900390625, 153580.751953125]

fib_js_rust_1_50 = [0.050048828125, 0.0078125, 0.02294921875, 0.146728515625, 2.258056640625, 
               1.85205078125, 19.000732421875, 168.48779296875, 1780.969970703125, 2839.147705078125,
               4553.25, 7300.285888671875, 11791.987060546875, 20112.083984375, 260460.83374023438]


climb_range = [100000, 500000, 1000000, 5000000, 10000000, 50000000, 100000000, 500000000, 1000000000]

climb_as_1_10 = [0.4169921875, 1.852783203125, 4.050048828125, 18.492919921875, 38.967041015625, 
                 156.115966796875, 296.77685546875, 1474.004150390625, 2915.2802734375]

climb_js_1_10 = [2.35205078125, 0.93994140625, 2.199951171875, 4.56689453125, 8.846923828125, 
                 45.02197265625, 84.59716796875, 329.665283203125, 676.06005859375]

climb_go_1_10 = [1.09814453125, 2.203125, 4.236083984375, 17.3291015625, 49.843017578125,
                 169.18896484375, 1586.651123046875, 2932.58984375, 14760.39111328125]

climb_rust_1_10 = [0.004150390625, 0.0048828125, 0.005126953125, 0.0048828125, 0.006103515625, 
                   0.006103515625, 0.005126953125, 0.00390625, 0.005126953125]

import matplotlib.pyplot as plt

## plot fib testing
# fig, ax1 = plt.subplots()
# ax1.plot(range_1_50, fib_as_1_50, 'ro', label='AssemblyScript')
# ax1.plot(range_1_50, fib_go_1_50, 'bs', label='Go')
# ax1.plot(range_1_50, fib_rust_1_50, 'g^', label='Rust')
# ax1.plot(range_1_50, fib_js_as_1_50, 'm*', label='JavaScript')

## fib plot 1 vs 1
# fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)

# ax1.plot(range_1_50, fib_as_1_50, 'ro', label='AssemblyScript wasm')
# ax1.plot(range_1_50, fib_js_as_1_50, 'b^', label='JavaScript')

# ax2.plot(range_1_50, fib_go_1_50, 'ro', label='Go wasm')
# ax2.plot(range_1_50, fib_js_go_1_50, 'b^', label='JavaScript')

# ax3.plot(range_1_50, fib_rust_1_50, 'ro', label='Rust wasm')
# ax3.plot(range_1_50, fib_js_rust_1_50, 'b^', label='JavaScript wasm')

# ax1.legend(loc="upper left")
# ax2.legend(loc="upper left")
# ax3.legend(loc="upper left")

# ax1.grid(True)

# ax2.grid(True)

# ax3.grid(True)
# ax3.set_xlabel('Fibonacci Sequence')
# ax3.set_ylabel('Time')

# fig.suptitle('Webassembly vs JavaScript (millisecond)', fontsize=16)

## P0 graph
# fib_p0 = [55, 103, 225, 1040, 10100, 
#           110000]
# range_1_6 = [1,5,10,15,20,25]
# fig, ax1 = plt.subplots()
# fig.suptitle('P0 (millisecond)', fontsize=16)
# ax1.plot(range_1_6, fib_p0, 'ro')
# ax1.set_xlabel('Fibonacci Sequence')
# ax1.set_ylabel('Time')

# plot climb method test 
# fig, ax1 = plt.subplots()
# ax1.plot(climb_range, climb_as_1_10, 'ro-', label='AssemblyScript')
# ax1.plot(climb_range, climb_go_1_10, 'bs-', label='Go')
# ax1.plot(climb_range, climb_rust_1_10, 'g^-', label='Rust')
# ax1.plot(climb_range, climb_js_1_10, 'm*-', label='JavaScript')

# fig.suptitle('Climb Increment by One (millisecond)', fontsize=16)
# ax1.set_xlabel('Input')
# ax1.set_ylabel('Time')
# ax1.legend()

## climb plot 1 vs 1
fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)

ax1.plot(climb_range, climb_as_1_10, 'ro', label='AssemblyScript wasm')
ax1.plot(climb_range, climb_js_1_10, 'b^', label='JavaScript')

ax2.plot(climb_range, climb_go_1_10, 'ro', label='Go wasm')
ax2.plot(climb_range, climb_js_1_10, 'b^', label='JavaScript')

ax3.plot(climb_range, climb_rust_1_10, 'ro', label='Rust wasm')
ax3.plot(climb_range, climb_js_1_10, 'b^', label='JavaScript wasm')

ax1.legend(loc="upper left")
ax2.legend(loc="upper left")
ax3.legend(loc="upper left")

ax1.grid(True)

ax2.grid(True)

ax3.grid(True)
ax3.set_xlabel('Itreated Times')
ax3.set_ylabel('Time')

fig.suptitle('Webassembly vs JavaScript (millisecond)', fontsize=16)

plt.show()

# size in each wasm file
# as 132 bytes
# go 1,374,791 bytes
# rust 1,543,076 bytes 
# p0 174 bytes

# classify front and backend