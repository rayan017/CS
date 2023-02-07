import pytest

from codebreaker import CodeBreaker
from seamcarve import SeamCarve

def compare_words(word1: str, word2: str):
    comparison_codebreaker = CodeBreaker(word1, word2)
    comparison_codebreaker.fill_similarities()
    return comparison_codebreaker.find_score()
    
def test_codebreaker():
    # TODO: add more assertions and/or test functions to test codebreaker
    assert compare_words("", "") == 0
    assert compare_words("code","cods")==1
    assert compare_words("inv","envi")==2
    assert compare_words("jovi","ovji")==2
    assert compare_words("code","code")==0
    assert compare_words("","bin")==3
    assert compare_words("i","bin")==2
    assert compare_words("eeve","even")==2

def test_seamcarve():
    # TODO: add more assertions and/or test functions to test seamcarve
    # cell E1 from 5x5 spreadsheet
    test_image = [[[255, 255, 255], [0, 0, 0], [125, 125, 125], [0, 0, 0],\
        [255, 255, 255]], [[0, 0, 0], [125, 125, 125], [0, 0, 0],
        [255, 255, 255], [0, 0, 0]], [[255, 255, 255], [125, 125, 125],
        [255, 255, 255], [0, 0, 0], [255, 255, 255]], [[0, 0, 0],
        [255, 255, 255], [125, 125, 125], [255, 255, 255], [0, 0, 0]], 
        [[255, 255, 255], [0, 0, 0], [255, 255, 255], [125, 125, 125],
        [255, 255, 255]]]
    expected_seam = [2, 1, 1, 2, 3]
    my_sc = SeamCarve(image_matrix = test_image)
    importance_vals = my_sc.calculate_importance_values()
    calculated_seam = my_sc.find_least_important_seam(importance_vals)
    test_image2=[[[33, 33, 33], [219, 219, 219], [17, 17, 17], [0, 0, 0], [2, 2, 2]], [[0, 0, 0], [12, 12, 12], [1, 1, 1], [25, 25, 25], [0, 0, 0]], [[255, 255, 255], [125, 125, 125], [255, 255, 255], [0, 0, 0], [255, 255, 255]], [[0, 0, 0], [255, 255, 255], [125, 125, 125], [255, 255, 255], [0, 0, 0]], [[25, 25, 25], [3, 3, 3], [29, 29, 29], [99, 99, 99], [180, 180, 180]]]
    my_sc2=SeamCarve(image_matrix=test_image2)
    importance_vals2=my_sc2.calculate_importance_values()
    expected_seam2=[3, 2, 1, 2, 2]
    test_image3=[[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]
    my_sc3=SeamCarve(image_matrix=test_image3)
    importance_vals3=my_sc3.calculate_importance_values()
    test_image4=[[[255,100,255],[50,100,0]],[[100,25,180],[235,200,0]]]
    my_sc4=SeamCarve(image_matrix=test_image4)
    importance_vals4=my_sc4.calculate_importance_values()
    test_image5=[[[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]], [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]], [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]], [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]], [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]]
    my_sc5=SeamCarve(image_matrix=test_image5)
    importance_vals5=my_sc5.calculate_importance_values()
    assert [0,0,0,0,0] == my_sc5.find_least_important_seam(importance_vals5)
    assert [1,1] == my_sc4.find_least_important_seam(importance_vals4)
    assert [0,0,0,0,0] == my_sc3.find_least_important_seam(importance_vals3)
    assert expected_seam == calculated_seam
    assert expected_seam2 == my_sc2.find_least_important_seam(importance_vals2)

