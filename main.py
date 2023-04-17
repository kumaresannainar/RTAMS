import app

print('**************************************Welcome to RTAMS**************************************')
print('--------------------------------------------------------------------------------------------')
print('Please do not write/delete images into source_imgs folder hereafter.')
print('If you do want to do so, please do stop the app and do the changes and then restart the app.')
print('--------------------------------------------------------------------------------------------')
while(1):
    key = input('Do you want to start attendance terminal? [Y/N]:')
    if(key in ['Y', 'y']):
        app.start()
    elif(key in ['N', 'n']):
        print('Thank you!!')
        print('--------------------------------------------------------------------------------------------')
        exit()
    else:
        print('Invalid option. Try again...')
        print('--------------------------------------------------------------------------------------------')
        continue