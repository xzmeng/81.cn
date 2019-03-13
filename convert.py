import os

SAVE_DIR = 'results_converted'
READ_DIR = 'results'
if not os.path.exists(SAVE_DIR):
    os.mkdir(SAVE_DIR)
# for dir_name in os.listdir(SAVE_DIR):
#     with open(os.path.join(SAVE_DIR, dir_name + '.txt'), 'w') as f:
#         for file_name in sorted(os.listdir(os.path.join(SAVE_DIR, dir_name))):
#             print(file_name)
#             with open(os.path.join(SAVE_DIR, dir_name, file_name)) as ff:
#                 f.write(ff.read())


for date in os.listdir(READ_DIR):
    cat_dir = os.path.join(READ_DIR, date)
    with open(os.path.join(SAVE_DIR, date + '.txt'), 'w') as f:
        for cat in sorted(os.listdir(cat_dir)):
            article_dir = os.path.join(cat_dir, cat)
            for article in sorted(os.listdir(article_dir)):
                with open(os.path.join(article_dir, article)) as ff:
                    f.write(ff.read())


