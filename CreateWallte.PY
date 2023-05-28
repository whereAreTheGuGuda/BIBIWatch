
from eth_account import Account
from eth_utils.hexadecimal import encode_hex
from eth_account.messages import encode_defunct
from xlsxwriter import Workbook
import argparse

def createWallet(name,wallet_count):
        workbook = Workbook(name + '.xlsx')  # 创建工作簿
        worksheet = workbook.add_worksheet('sheet1')        #创建新的sheet
        rowIndex = 1
        for i in range(wallet_count):
            Account.enable_unaudited_hdwallet_features()
            account, mnemonic = Account.create_with_mnemonic(language = "english")
            addressIndex = 'A' + str(rowIndex)
            walletIndex = 'B' + str(rowIndex)
            hexIndex = 'C' + str(rowIndex)
            worksheet.write(addressIndex, account.address)
            worksheet.write(walletIndex,mnemonic)
            worksheet.write(hexIndex,account.key.hex())
            rowIndex += 1
        workbook.close()
        
if __name__ == '__main__':
        parser = argparse.ArgumentParser(
        description='Writing the input json data to the corresponding .xls template file and save ')
        # 这里的描述会出现在 usage下方 表明这个程序的作用是什么
        parser.add_argument("--name", type=str, default="wallet")
        parser.add_argument("--wallet_count", type=int, default=10)
        args = parser.parse_args()
        name = args.name
        wallet_count = args.wallet_count
        createWallet(name,wallet_count)