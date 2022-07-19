from optparse import Values
from pymodbus3.client.sync import ModbusTcpClient
from pymodbus3.constants import Endian
from pymodbus3.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from logger import *
from colorama import Fore


# import logging
# # --------------------------------------------------------------------------- #
# # log config
# # --------------------------------------------------------------------------- #
# FORMAT = (
#     "%(asctime)-15s %(threadName)-15s "
#     "%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s"
# )
# logging.basicConfig(format=FORMAT)
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)


UNIT = 0x01

class OperaMetrix_ModbusTCP_client():
    def __init__(self,host='192.168.0.90'):
        self.client = ModbusTcpClient(host)

    def connect(self):
        # --------------------------------------------------------------------------- #
        # Configuration et connexion au client
        # --------------------------------------------------------------------------- #
        if self.client.connect():
            log.debug("Connected to the client")
        else:
            log.debug("CONNEXION ERROR")

    def close(self): 
        # --------------------------------------------------------------------------- #
        # Close client
        # --------------------------------------------------------------------------- #
        if self.client.close():
            log.debug("disconnected from client")   

    def Read_addr(self,addr,Type = 'float',verbose = True):
        """ Allows to read a value from modbus API with IP address 192.168.0.90 
        ## Pameters:
        - addr:  the address of the infomation you want to read
        - Type: ( default : 'float' ) the type of data stored at this address: 
            - you can specify float, string, bool, 16uint or 8uint
        ## Returns:
        - value of the address asked
        """
        # --------------------------------------------------------------------------- #
        # Test lecture et décodage Modbus
        # --------------------------------------------------------------------------- #
        response = self.client.read_holding_registers(int(addr),count=3)
        value = None
        # print (response)
        # log.debug(f"\n Voici la réponse brute de PyModbus: {response}\n")
        decoder = BinaryPayloadDecoder.from_registers(registers=response.registers, endian=Endian.Big)
        # log.debug(f"Voici le décoder: {decoder}")
        if Type == 'float':
            value = decoder.decode_32bit_float()
        elif Type == 'string':
            value = decoder.decode_string(8)
        elif Type == 'bool':
            b = addr%int(addr)
            if b == 0:
                value = decoder.decode_bits()[0]
            elif 0.051>b and b>0.049:
                value = decoder.decode_bits()[1]
            elif 0.11>b and b>0.099:
                value = decoder.decode_bits()[2]
            else:
                return False
        elif Type == '16uint':
            value = decoder.decode_16bit_int()
        elif Type == '8uint':
            value = decoder.decode_8bit_uint()
        else :
            log.error ("Wrong type given")
            exit()
        if verbose:
            log.info (Fore.RED + f"Here is the response at {addr}: {value}" + Fore.RESET)
        return value
        

    def Read_all_addr(self):
        """Allows to read all 120 addresses from the API
        # Returns:
        - list of 120 rows of things contined in the addresses and 2 columns ( address / actual value )
        """
        A_float = [x for x in range(0,54,2)]
        B_bool = [54, 54.05 , 54.1]
        C_float = [x for x in range(55,77,2) ]
        D_bool = [75 , 75.05 , 75.1]
        E_float = [76,78,80] 
        F_bool = [82]
        G_float = [x for x in range(83,113,2)]
        H_bool = [113]
        I_uint = [114]
        J_usint = [x for x in range(115,118,0.5)]
        K_udint = [118]
        L_bool = [120]
        VALUES = [[],[]]
        for i in A_float:
            VALUES[0].append(i)
            VALUES[1].append(self.Read_addr(i,'float'))
        for i in B_bool:
            VALUES[0].append(i)
            VALUES[1].append(self.Read_addr(i,'bool'))
        for i in C_float:
            VALUES[0].append(i)
            VALUES[1].append(self.Read_addr(i,'float'))
        for i in D_bool:
            VALUES[0].append(i)
            VALUES[1].append(self.Read_addr(i,'bool'))
        for i in E_float:
            VALUES[0].append(i)
            VALUES[1].append(self.Read_addr(i,'float'))
        for i in F_bool:
            VALUES[0].append(i)
            VALUES[1].append(self.Read_addr(i,'bool'))
        for i in G_float:
            VALUES[0].append(i)
            VALUES[1].append(self.Read_addr(i,'float'))
        for i in H_bool:
            VALUES[0].append(i)
            VALUES[1].append(self.Read_addr(i,'bool'))
        # for i in I_uint:
        #     VALUES[0].append(i)
        #     VALUES[1].append(self.Read_addr(i,'float'))
        # for i in J_usint:
        #     VALUES[0].append(i)
        #     VALUES[1].append(self.Read_addr(i,'float'))
        # for i in K_udint:
        #     VALUES[0].append(i)
        #     VALUES[1].append(self.Read_addr(i,'bool'))
        for i in L_bool:
            VALUES[0].append(i)
            VALUES[1].append(self.Read_addr(i,'bool'))
    
    def Write_addr(self,addr,object,Type = 'float'):
        """ Allows to write a value to a modbus API with IP address 192.168.0.90 
        ## Pameters:
        - addr:  the address of the infomation you want to write
        - object: the type of data you want to be stored at this address
        - Type: ( default : 'float' ) the type of data stored at this address: 
            - you can specify float, string, bool, 16 uint or 8int
        """
        # --------------------------------------------------------------------------- #
        # écriture
        # --------------------------------------------------------------------------- #
        builder = BinaryPayloadBuilder(endian = Endian.Big)
        if Type == 'float':
            builder.add_32bit_float(object)
        elif Type == 'string':
            builder.add_string(object)
        elif Type == 'bool':
            decimales = addr%int(addr)
            b = int(addr)
            if decimales == 0:
                towrite = [object,self.Read_addr(b+0.05,Type,False),self.Read_addr(b+0.1,Type,False),self.Read_addr(b+0.15,Type,False),self.Read_addr(b+0.2,Type,False),self.Read_addr(b+0.25,Type,False),self.Read_addr(b+0.3,Type,False),self.Read_addr(b+0.4,Type,False)]
                builder.add_bits(towrite)
            elif 0.51>decimales and decimales>0.049:
                towrite = [self.Read_addr(b,Type,False),object,self.Read_addr(b+0.1,Type,False),self.Read_addr(b+0.15,Type,False),self.Read_addr(b+0.2,Type,False),self.Read_addr(b+0.25,Type,False),self.Read_addr(b+0.3,Type,False),self.Read_addr(b+0.4,Type,False)]
                builder.add_bits(towrite)
            elif 0.11>decimales and decimales>0.099:
                towrite = [self.Read_addr(b,Type,False),self.Read_addr(b+0.05,Type,False),object,self.Read_addr(b+0.15,Type,False),self.Read_addr(b+0.2,Type,False),self.Read_addr(b+0.25,Type,False),self.Read_addr(b+0.3,Type,False),self.Read_addr(b+0.4,Type,False)]                
                builder.add_bits(towrite)
            logging.info(f"towrite: {towrite}")
        elif Type == '16uint':
            b = addr%int(addr)
            if b == 0:
                builder.add_16bit_uint(object)
            elif 0.51>b and b>0.049:
                builder.add_16bit_uint(object)            
        elif Type == '8int':
            builder.add_8bit_uint(object)
            


        payload = builder.build()
        # print (f"TEEEEEST {payload}\n")
        if Type != 'bool':
            self.client.write_registers(addr,payload,skip_encode=True)
        else :
            self.client.write_registers(b,payload,skip_encode=True)
        log.info (Fore.RED + f"writing {object} in {addr}"+ Fore.RESET)
        
  



# while (1):
#     addr = int(input("\nEntrer l'adresse de lecture: "))
#     Read_addr(83)
#     sleep(2)

# Myclient = OperaMetrix_ModbusTCP_client()
# Myclient.connect()
# testa = 101
# Myclient.Read_addr(testa)
# sleep(1)
# Myclient.Write_addr(testa,2.5)
# sleep(1)
# Myclient.Read_addr(testa)
# Myclient.close()