# Example Description

Example for IPV6.

# HW Configuration

None

# SW configuration

1. `lwipopts.h`
	```C
	#define LWIP_IPV6					1
	```

2. `src/include/lwip/opt.h`
	```C
	#define MEMP_NUM_MLD6_GROUP			6
	```
	If MEMP_NUM_MLD6_GROUP is not big enough, it may occur
	```
	[ERROR] Register to ipv6 multicast group failed
	```

3. `example_ipv6.h`
	```C
	#define UDP_SERVER_IP    "fe80:0000:0000:0000:cd3c:24de:386d:9ad1"
	#define TCP_SERVER_IP    "fe80:0000:0000:0000:cd3c:24de:386d:9ad1"
	```
	Change the ipv6 address based on output of server example to run client.

4. How to use:
   - Run `./build.py -a ipv6` under project path, e.g. `amebasmart_gcc_project/`, to generate images.
   - `Download` images to board by Ameba Image Tool.

# Expect result

A IPV6 example thread will be started automatically when booting.

Need to run server example first to get the server IP and use this IP for client example.

# Note

Enable one example at one time to verify client or server examples.

Modify `UDP_SERVER_IP` and `TCP_SERVER_IP` for client example according to server output.

# Supported IC

- AmebaSmart
- AmebaLite
- AmebaDplus
