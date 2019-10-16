# matcher
# - explanation_leaf - pks_pos_section - syn_section - sensensed-item
# - explanation_leaf - pks - etymology_section - syn_section - senced-item
# - lang_section - syn_section - sensed-item

for l_node in toc.find_lang_section():
    for pos_node in l_node.find_pos_section():
        for e_node in pos_node.find_explanations():
            pass

