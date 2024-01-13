import math

from PIL import Image, ImageDraw, ImageFilter
from collections import  Counter
import random


def distance(pos1, pos2):
    return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**0.5
def convertAngleToVector(angle):
    return  (math.sin(angle / 57.2958), math.cos(angle / 57.2958))
def convertVectorToAngle(vector):
    if vector[1]==0 and vector[0]==0:
        return None
    elif vector[1] == 0 and vector[0] > 0:
        return 90
    elif vector[1] == 0 and vector[0] < 0:
        return 270
    elif vector[1] > 0 and vector[0] == 0:
        return 0
    elif vector[1] < 0 and vector[0] == 0:
        return 180

    if vector[0] > 0 and vector[1] > 0:
        return (math.atan(vector[0] / vector[1]))*57.2958
    if vector[0] > 0 and vector[1] < 0:
        return (math.atan(vector[0] / vector[1]))*57.2958
    if vector[0] < 0 and vector[1] < 0:
        return (math.atan(vector[0] / vector[1]))*57.2958
    if vector[0] < 0 and vector[1] > 0:
        return (math.atan(vector[0] / vector[1]))*57.2958


def genSquaresGradientBackground(img_size, divisions, bias, separator, separator_width):
    img = Image.new(mode="RGB", size=(img_size, img_size))
    for i in range(divisions):
        for j in range(divisions):
            start_point = (int(img_size/divisions*j), int(img_size/divisions*i))
            color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
            bias = [bias[0], bias[1], bias[2]]
            for n in range(3):
                r = random.randint(0, 1)
                if r == 0:
                    bias[n] = -bias[n]
            for k in range(int(img_size/divisions)):
                color = [color[0]+bias[0], color[1]+bias[1], color[2]+bias[2]]
                for l in range(0,3):
                    if color[l] < 0:
                        color[l] = 0
                    if color[l] > 255:
                        color[l] = 255
                for z in range(int(img_size/divisions)):
                    t_col = (color[0], color[1], color[2])
                    img.putpixel((start_point[0]+z, start_point[1]+k), t_col)
    for i in range(divisions):
        for j in range(img_size):
            for k in range(separator_width):
                img.putpixel((j, int(i*img_size/divisions)+k), separator)
    for i in range(divisions):
        for j in range(img_size):
            for k in range(separator_width):
                img.putpixel((int(i*img_size/divisions+k), j), separator)
    start_point_x = img_size-separator_width
    for i in range(img_size):
        for j in range(separator_width):
            img.putpixel((start_point_x+j, i), separator)
    start_point_y = img_size-separator_width
    for i in range(img_size):
        for j in range(separator_width):
            img.putpixel((i, start_point_y+j), separator)
    return img


def genSquaresCirclesGradientBackground(img_size, divisions, bias, separator, separator_width, round_outline_width):
    img = Image.new(mode="RGB", size=(img_size, img_size))
    for i in range(divisions):
        for j in range(divisions):
            start_point = (int(img_size/divisions*j), int(img_size/divisions*i))
            color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
            bias = [bias[0], bias[1], bias[2]]
            for n in range(3):
                r = random.randint(0, 1)
                if r == 0:
                    bias[n] = -bias[n]
            for k in range(int(img_size/divisions)):
                color = [color[0]+bias[0], color[1]+bias[1], color[2]+bias[2]]
                for l in range(0,3):
                    if color[l] < 0:
                        color[l] = 0
                    if color[l] > 255:
                        color[l] = 255
                for z in range(int(img_size/divisions)):
                    t_col = (color[0], color[1], color[2])
                    img.putpixel((start_point[0]+z, start_point[1]+k), t_col)

            # color=[255-color[0], 255-color[1], 255-color[2]]
            color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
            reference_point = (int(img_size/divisions*j+round(img_size/divisions/2)), int(img_size/divisions*i))
            for k in range(int(round(img_size/divisions))):
                color = [color[0]+bias[0], color[1]+bias[1], color[2]+bias[2]]
                for l in range(0,3):
                    if color[l] < 0:
                        color[l] = 0
                    if color[l] > 255:
                        color[l] = 255
                slk = k
                # if k >= img_size/divisions/2:
                #     k=img_size/divisions-k
                segmentLenght = int(round(2*(k*(img_size/divisions-slk))**0.5))
                start_point = (int(round(reference_point[0]-segmentLenght/2)), int(round(img_size/divisions*i+k)))
                for z in range(segmentLenght):
                    img.putpixel((start_point[0]+z, start_point[1]), (color[0], color[1], color[2]))

    for i in range(divisions):
        for j in range(img_size):
            for k in range(separator_width):
                img.putpixel((j, int(i*img_size/divisions)+k), separator)
    for i in range(divisions):
        for j in range(img_size):
            for k in range(separator_width):
                img.putpixel((int(i*img_size/divisions+k), j), separator)
    start_point_x = img_size-separator_width
    for i in range(img_size):
        for j in range(separator_width):
            img.putpixel((start_point_x+j, i), separator)
    start_point_y = img_size-separator_width
    for i in range(img_size):
        for j in range(separator_width):
            img.putpixel((i, start_point_y+j), separator)
    return img

def genFlame(img_size_tuple,
             background_color,
             start_gradient_color,
             end_gradient_color,
             squares_qnty,
             start_size,
             end_size,
             is_outline,
             outline_color_offset,
             outline_width,
             solid_outline_color,
             random_color_range,
             random_size_range):
    img = Image.new("RGB", img_size_tuple)
    img_array = []
    sizes_list = []
    colors_list_R = []
    colors_list_G = []
    colors_list_B = []
    for i in range(img_size_tuple[0]):
        img_array.append([])
        for j in range(img_size_tuple[1]):
            img_array[i].append(background_color)
    step_pos = (img_size_tuple[1]-end_size)/squares_qnty
    curr_pos_y = 0
    if start_size < end_size:
        curr_size = start_size
        size_diff = end_size - start_size
        size_step = size_diff / squares_qnty
        for i in range(squares_qnty):
            sizes_list.append(int(round(curr_size)))
            curr_size += size_step
    else:
        curr_size = start_size
        size_diff = start_size - end_size
        size_step = size_diff / squares_qnty
        for i in range(squares_qnty):
            sizes_list.append(int(round(curr_size)))
            curr_size -= size_step

    if start_gradient_color[0] > end_gradient_color[0]:
        curr_color = start_gradient_color[0]
        color_diff = start_gradient_color[0] - end_gradient_color[0]
        color_step = color_diff / squares_qnty
        for i in range(squares_qnty):
            colors_list_R.append(int(round(curr_color)))
            curr_color -= color_step
    else:
        curr_color = start_gradient_color[0]
        color_diff = end_gradient_color[0] - start_gradient_color[0]
        color_step = color_diff / squares_qnty
        for i in range(squares_qnty):
            colors_list_R.append(int(round(curr_color)))
            curr_color += color_step

    if start_gradient_color[1] > end_gradient_color[1]:
        curr_color = start_gradient_color[1]
        color_diff = start_gradient_color[1] - end_gradient_color[1]
        color_step = color_diff / squares_qnty
        for i in range(squares_qnty):
            colors_list_G.append(int(round(curr_color)))
            curr_color -= color_step
    else:
        curr_color = start_gradient_color[1]
        color_diff = end_gradient_color[1] - start_gradient_color[1]
        color_step = color_diff / squares_qnty
        for i in range(squares_qnty):
            colors_list_G.append(int(round(curr_color)))
            curr_color += color_step

    if start_gradient_color[2] > end_gradient_color[2]:
        curr_color = start_gradient_color[2]
        color_diff = start_gradient_color[2] - end_gradient_color[2]
        color_step = color_diff / squares_qnty
        for i in range(squares_qnty):
            colors_list_B.append(int(round(curr_color)))
            curr_color -= color_step
    else:
        curr_color = start_gradient_color[2]
        color_diff = end_gradient_color[2] - start_gradient_color[2]
        color_step = color_diff / squares_qnty
        for i in range(squares_qnty):
            colors_list_B.append(int(round(curr_color)))
            curr_color += color_step

    for i in range(squares_qnty):
        size = sizes_list[i] + random.randint(-random_size_range, random_size_range)
        start_pos = (random.randint(0, img_size_tuple[0])-size, curr_pos_y)
        color = (colors_list_R[i]+random.randint(-random_color_range, random_color_range),
                 colors_list_G[i]+random.randint(-random_color_range, random_color_range),
                 colors_list_B[i]+random.randint(-random_color_range, random_color_range))
        save_color = color
        for y in range(size):
            for x in range(size):
                if is_outline:
                    color = save_color
                    if (x < outline_width) or (x > size-outline_width-1) or (y < outline_width) or (y > size-outline_width-1):
                        if outline_color_offset == True:
                            color = solid_outline_color
                        else:
                            color = (color[0]+outline_color_offset[0], color[1]+outline_color_offset[1], color[2]+outline_color_offset[2])
                            if color[0] > 255: color = (255, color[1], color[2])
                            if color[0] < 0: color = (0, color[1], color[2])
                            if color[1] > 255: color = (color[0], 255, color[2])
                            if color[1] < 0: color = (color[0], 0, color[2])
                            if color[2] > 255: color = (color[0], color[1], 255)
                            if color[2] < 0: color = (color[0], color[1], 0)
                        pass
                img_array[int(start_pos[0]+x)][int(start_pos[1]+y)] = color
        curr_pos_y+=step_pos
    for i in range(len(img_array)):
        for j in range(len(img_array[i])):
            img.putpixel((i, j), img_array[i][j])

    return img

####### WORK IN PROGRESS #######
def genCurvesBackground(img_size,
                        background_color,
                        lines_steps,
                        line_lenght,
                        lines_to_new_step,
                        angle_states_change_qnty,
                        angle_move_range,
                        angle_move_bias_range,
                        lines_start_gradient_color,
                        lines_end_gradient_color):
    img = Image.new(mode="RGB", size=(img_size, img_size), color=background_color)
    img_array = []

    for i in range(img_size):
        img_array.append([])
        for j in range(img_size):
            img_array[i].append((background_color, int()))


    pos = tuple()
    angle = int()
    lines_starts = []
    angle_move = int()
    angle_move_bias = int()
    bias_state = bool()
    general_placed_pixels = []

    pos = (random.randint(0, img_size), random.randint(0, img_size))
    angle = (random.randint(0, 360))

    img_array[pos[1]][pos[0]] = (lines_start_gradient_color, angle)
    lines_starts.append((pos, angle))

    for i in range(lines_steps):
        for j in lines_starts:
            color_step = ((lines_end_gradient_color[0]-lines_start_gradient_color[0])/line_lenght,
                          (lines_end_gradient_color[1]-lines_start_gradient_color[1])/line_lenght,
                          (lines_end_gradient_color[2]-lines_start_gradient_color[2])/line_lenght)
            pos = j[0]
            angle = j[1]
            if type(line_lenght) is tuple:
                lenght = random.randint(line_lenght[0], line_lenght[1])
            else:
                lenght = line_lenght
            lenght_to_change_state = lenght/angle_states_change_qnty
            state_change_counter = 0
            states = (True, False)
            r = random.randint(0, 1)
            bias_state = states[r]
            placed_pixels = []
            angle_move = random.randint(angle_move_range[0], angle_move_range[1])
            angle_move = angle_move/100
            angle_move_bias = random.randint(angle_move_bias_range[0], angle_move_bias_range[1])
            color = lines_start_gradient_color
            for k in range(lenght):
                state_change_counter += 1
                if state_change_counter >= lenght_to_change_state:
                    if bias_state:
                        bias_state = False
                        state_change_counter = 0
                    else:
                        bias_state = True
                        state_change_counter = 0

                if (pos[0] >= img_size-1):
                    pos = (0, pos[1])
                if (pos[0] < 0):
                    pos = (img_size-1, pos[1])
                if (pos[1] >= img_size-1):
                    pos = (pos[0], 0)
                if (pos[1] < 0):
                    pos = (pos[0], img_size-1)

                img_pos = (round(pos[0]), round(pos[1]))
                img_array[img_pos[1]][img_pos[0]] = ((round(color[0]), round(color[1]), round(color[0])), angle)
                placed_pixels.append((img_pos, angle))
                vector = convertAngleToVector(angle)
                pos = (pos[0] + vector[0], pos[1] + vector[1])

                if bias_state:
                    angle += angle_move
                    angle_move += angle_move_bias
                else:
                    angle -= angle_move
                    angle_move += angle_move_bias
                color = (color[0] + color_step[0], color[1] + color_step[1], color[2] + color_step[2])
            general_placed_pixels.append(placed_pixels)
        for j in general_placed_pixels:
            for k in range(lines_to_new_step):
                index = random.randint(0, len(j)-1)
                lines_starts.append(j[index])



    for i in range(img_size):
        for j in range(img_size):
            img.putpixel((j, i), img_array[j][i][0])

    return img


def genMappingWarPic(image, attack_color, defence_color, steps, break_intensity, break_frequency):
    img_size = image.size
    img = Image.new("RGB", img_size)
    img.paste(image)
    img_array = []

    for i in range(img_size[0]):
        img_array.append([])
        for j in range(img_size[1]):
            img_array[i].append(img.getpixel((i, j)))

    for i in range(steps):
        attack = []
        defence = []
        for j in range(img_size[0]):
            for k in range(img_size[1]):
                if img_array[j][k] == attack_color:
                    attack.append((j, k))
                if img_array[j][k] == defence_color:
                    defence.append((j, k))
        bordering_pixels = []
        for j in attack:
            if j[0] + 1 < img_size[0]:
                if img_array[j[0] + 1][j[1]] == defence_color:
                    bordering_pixels.append((j[0] + 1, j[1]))
            if j[0] - 1 >= 0:
                if img_array[j[0] - 1][j[1]] == defence_color:
                    bordering_pixels.append((j[0] - 1, j[1]))
            if j[1] + 1 < img_size[1]:
                if img_array[j[0]][j[1] + 1] == defence_color:
                    bordering_pixels.append((j[0], j[1] + 1))
            if j[1] - 1 >= 0:
                if img_array[j[0]][j[1] - 1] == defence_color:
                    bordering_pixels.append((j[0], j[1] - 1))

        for j in range(break_intensity):
            bordering_pixels_t = bordering_pixels
            for k in bordering_pixels:
                if random.randint(0, 100000)/1000 < break_frequency:
                    if k[0] + 1 < img_size[0]:
                        if img_array[k[0] + 1][k[1]] == defence_color:
                            bordering_pixels_t.append((k[0] + 1, k[1]))
                    if k[0] - 1 >= 0:
                        if img_array[k[0] - 1][k[1]] == defence_color:
                            bordering_pixels_t.append((k[0] - 1, k[1]))
                    if k[1] + 1 < img_size[1]:
                        if img_array[k[0]][k[1] + 1] == defence_color:
                            bordering_pixels_t.append((k[0], k[1] + 1))
                    if k[1] - 1 >= 0:
                        if img_array[k[0]][k[1] - 1] == defence_color:
                            bordering_pixels_t.append((k[0], k[1] - 1))
            bordering_pixels = bordering_pixels_t

        # for j in range(img_size[0]):
        #     for k in range(img_size[1]):
        #         if j != img_size[0]-1:
        #             if img_array[j][k] == img_array[j+1][k]:
        #                 bordering_pixels[(j, k)] = (j+1, k)
        #         elif j != 0:
        #             if img_array[j][k] == img_array[j-1][k]:
        #                 bordering_pixels[(j, k)] = (j-1, k)
        #         elif k != img_size[1]-1:
        #             if img_array[j][k] == img_array[j][k+1]:
        #                 bordering_pixels[(j, k)] = (j, k+1)
        #         elif k != 0:
        #             if img_array[j][k] == img_array[j][k-1]:
        #                 bordering_pixels[(j, k)] = (j, k-1)
        pixels_under_attack = Counter(bordering_pixels)
        for j in pixels_under_attack.keys():
            img_array[j[0]][j[1]] = attack_color

    for i in range(img_size[0]):
        for j in range(img_size[1]):
            img.putpixel((i, j), img_array[i][j])
    return img

def smoke1(image, background_color, color_intensity_factor, shadow_factor, max_dist, shf_increase_factor):
    img_size = image.size
    img = Image.new("RGB", img_size)
    img.paste(image)
    img_array = []

    for i in range(img_size[0]):
        img_array.append([])
        for j in range(img_size[1]):
            img_array[i].append(img.getpixel((i, j)))

    lines_colors = []
    for i in img_array:
        for j in i:
            if j != background_color and lines_colors.count(j) == 0:
                lines_colors.append(j)

    line_poses = {} # {цвет: координаты}
    cntr = 0
    for i in lines_colors:
        line_poses[i] = []
    for i in lines_colors:
        for j in range(len(img_array)):
            for k in range(len(img_array[j])):
                if img_array[j][k] == i:
                    # line_poses.append(((j, k), lines_colors[i]))
                    line_poses[i].append((j, k))

    for i in line_poses.keys():
        # line_poses = []
        # for j in range(len(img_array)):
        #     for k in range(len(img_array[j])):
        #         if img_array[j][k] == i:
        #             line_poses.append((j, k))
        cntr = 0
        for n in line_poses[i]:
            for j in range(len(img_array)):
                for k in range(len(img_array[j])):
                    curr_color = img_array[j][k]
                    dist = distance((j, k), n)
                    if dist == 0:
                        dist = 1
                    if dist > max_dist:
                        continue
                    set_color = (i[0]/(dist/color_intensity_factor),
                                 i[1]/(dist/color_intensity_factor),
                                 i[2]/(dist/color_intensity_factor))
                    # diff = (set_color[0]-curr_color[0],
                    #         set_color[1]-curr_color[1],
                    #         set_color[2]-curr_color[2])
                    # diff = (diff[0]*shadow_factor, diff[1]*shadow_factor, diff[2]*shadow_factor)
                    # set_col0 = curr_color[0] + diff[0]
                    # set_col1 = curr_color[1] + diff[1]
                    # set_col2 = curr_color[2] + diff[2]

                    if set_color[0] < 0:
                        set_color = (0, set_color[1], set_color[2])
                    if set_color[1] < 0:
                        set_color = (set_color[0], 0, set_color[2])
                    if set_color[2] < 0:
                        set_color = (set_color[0], set_color[1], 0)

                    set_col0 = curr_color[0] + set_color[0] * shadow_factor
                    set_col1 = curr_color[1] + set_color[1] * shadow_factor
                    set_col2 = curr_color[2] + set_color[2] * shadow_factor

                    img_array[j][k] = (set_col0, set_col1, set_col2)

                    # img_array[j][k] = set_color
            cntr+=1
            print(f"{cntr} / {len(line_poses[i])}")
        shadow_factor *= shf_increase_factor

    for i in range(img_size[0]):
        for j in range(img_size[1]):
            if img_array[i][j][0] > 255:
                img_array[i][j] = (255, img_array[i][j][1], img_array[i][j][2])
            if img_array[i][j][1] > 255:
                img_array[i][j] = (img_array[i][j][0], 255, img_array[i][j][2])
            if img_array[i][j][2] > 255:
                img_array[i][j] = (img_array[i][j][0], img_array[i][j][1], 255)
    for i in range(img_size[0]):
        for j in range(img_size[1]):
            img.putpixel((i, j), (round(img_array[i][j][0]),round(img_array[i][j][1]), round(img_array[i][j][2])))
    return img

def genCloudsBackground(image, colors, steps, break_frequency, bias, max_dist):
    img_size = image.size
    img = Image.new("RGB", img_size)
    img.paste(image)
    img_array = []
    for i in range(img_size[0]):
        img_array.append([])
        for j in range(img_size[1]):
            img_array[i].append(img.getpixel((i, j)))

    color_counter_debug = 0
    for col in colors:
        # print("color: " + str(color_counter_debug))
        steps_counter_debug = 0
        for i in range(steps):
            # print("step: " + str(steps_counter_debug))
            img_array_t = img_array
            for j in range(len(img_array)):
                for k in range(len(img_array[j])):
                    if img_array[j][k] == col:
                        if j < len(img_array)-1:
                            if (img_array[j+1][k] != col) & (random.random() < break_frequency):
                                img_array_t[j+1][k] = col
                        if j > 0:
                            if (img_array[j-1][k] != col) & (random.random() < break_frequency):
                                img_array_t[j-1][k] = col
                        if k < len(img_array[0])-1:
                            if (img_array[j][k+1] != col) & (random.random() < break_frequency):
                                img_array_t[j][k+1] = col
                        if k > 0:
                            if (img_array[j][k-1] != col) & (random.random() < break_frequency):
                                img_array_t[j][k-1] = col
            img_array = img_array_t
            steps_counter_debug += 1

        bordering_pixels = []
        bordering_pixels_counter_debug = 0
        for j in range(len(img_array)):
            # print("bordering_pixels: " + str(bordering_pixels_counter_debug))
            for k in range(len(img_array[j])):
                if img_array[j][k] == col:
                    if j < len(img_array) - 1:
                        if img_array[j + 1][k] != col:
                            bordering_pixels.append((j + 1, k))
                    if j > 0:
                        if img_array[j - 1][k] != col:
                            bordering_pixels.append((j - 1, k))
                    if k < len(img_array[0]) - 1:
                        if img_array[j][k + 1] != col:
                            bordering_pixels.append((j, k + 1))
                    if k > 0:
                        if img_array[j][k - 1] != col:
                            bordering_pixels.append((j, k - 1))
            bordering_pixels_counter_debug += 1

        shadow_counter_debug = 0
        for i in range(len(img_array)):
            # print("shadow: " + str(shadow_counter_debug))
            for j in range(len(img_array[i])):
                if img_array[i][j] == col:
                    min_dist = max_dist
                    for k in bordering_pixels:
                        dist = distance(k, (i, j))
                        if dist > max_dist:
                            continue
                        if dist < min_dist:
                            min_dist = dist
                    # colR = round(col[0]-(bias[0]/max_dist)*(max_dist-min_dist))
                    # colG = round(col[1]-(bias[1]/max_dist)*(max_dist-min_dist))
                    # colB = round(col[2]-(bias[2]/max_dist)*(max_dist-min_dist))

                    bias_col_R = col[0] - (255 - col[0])
                    bias_col_G = col[1] - (255 - col[1])
                    bias_col_B = col[2] - (255 - col[2])

                    processed_bias = (bias_col_R * bias[0], bias_col_G * bias[1], bias_col_B * bias[2])

                    colR = round(col[0] - (processed_bias[0] / max_dist) * (max_dist - min_dist))
                    colG = round(col[1] - (processed_bias[1] / max_dist) * (max_dist - min_dist))
                    colB = round(col[2] - (processed_bias[2] / max_dist) * (max_dist - min_dist))

                    # if colR > 255:
                    #     colR = 255
                    # if colG > 255:
                    #     colG = 255
                    # if colB > 255:
                    #     colB = 255
                    # if colR < 0:
                    #     colR = 0
                    # if colG < 0:
                    #     colG = 0
                    # if colB < 0:
                    #     colB = 0
                    color = (colR, colG, colB)
                    img_array[i][j] = color
                    # print(color)
            shadow_counter_debug += 1


        color_counter_debug += 1


    for i in range(len(img_array)):
        for j in range(len(img_array[i])):
            img.putpixel((i, j), img_array[i][j])

    return img

def genDirectedCloud1(image, color, angles, dist_power, angle_diff_power):
    img = Image.new(mode="RGB", size=(image.size))
    img.paste(image)

    point = None

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            curr_color = img.getpixel((i, j))
            if curr_color != (0, 0, 0):
                print(curr_color)
            if curr_color == color:
                point = (i, j)
                break

    if point == None:
        return

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            for k in angles:
                cord_diff = (point[0]-i, point[1]-j)
                dist = distance((i, j), point)
                if dist == 0:
                    dist = 1
                curr_angle = convertVectorToAngle(cord_diff)
                angle_diff = abs(curr_angle-k)
                adding_color_factor = (((1/dist**dist_power))/angle_diff**angle_diff_power)
                colorR = color[0] * adding_color_factor
                if colorR > 255:
                    colorR = 255
                colorG = color[1] * adding_color_factor
                if colorG > 255:
                    colorG = 255
                colorB = color[2] * adding_color_factor
                if colorB > 255:
                    colorB = 255

                img.putpixel((i, j), (round(colorR), round(colorG), round(colorB)))
    return img

# TODO
def genDirectedCloud(image, color, angles, dist_factor, angle_dist_factor, max_dist, general_factor):
    img = Image.new(mode="RGB", size=(image.size))
    img.paste(image)

    point = None

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            curr_color = img.getpixel((i, j))
            if curr_color != (0, 0, 0):
                print(curr_color)
            if curr_color == color:
                point = (i, j)
                break

    if point == None:
        return

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            for k in angles:
                cord_diff = (point[0]-i, point[1]-j)
                dist = distance((i, j), point)
                if dist == 0:
                    adding_color_factor = 1 * general_factor
                elif dist > max_dist:
                    continue
                else:
                    curr_angle = convertVectorToAngle(cord_diff)
                    angle_diff = abs(curr_angle-k)
                    if angle_diff > 180:
                        angle_diff = 360 - angle_diff
                    if angle_diff > 90:
                        angle_dist = dist
                    else:
                        angle_dist = dist*math.sin(angle_diff/57.2958)


                    max_factor = (max_dist*angle_dist_factor*max_dist*dist_factor)
                    curr_factor = (angle_dist*angle_dist_factor*dist*dist_factor)
                    adding_color_factor = ((max_factor-curr_factor) / max_factor) * general_factor

                colorR = color[0] * adding_color_factor
                if colorR > 255:
                    colorR = 255
                colorG = color[1] * adding_color_factor
                if colorG > 255:
                    colorG = 255
                colorB = color[2] * adding_color_factor
                if colorB > 255:
                    colorB = 255

                pixel = img.getpixel((i, j))
                pixel = [pixel[0], pixel[1], pixel[2]]
                pixel[0] += colorR
                pixel[1] += colorG
                pixel[2] += colorB
                pixel = (round(pixel[0]), round(pixel[1]), round(pixel[2]))
                img.putpixel((i, j), pixel)
    return img


# genDirectedCloud(image=Image.open("bkgr.png"),
#                  color=(255, 0, 0),
#                  angles=[0],
#                  dist_factor=10,
#                  angle_dist_factor=0.3,
#                  max_dist=1000,
#                  general_factor=0.25).show()


# genCloudsBackground(image=Image.open("cld0.png"),
#                     colors=[(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)],
#                     steps=30,
#                     break_frequency=0.1,
#                     bias=(2, -2, 2),
#                     max_dist=27).show()

# img = Image.open("smoke.png")
# smoke1(image=img,
#        background_color=(0, 0, 0),
#        color_intensity_factor=1,
#        shadow_factor=0.5,
#        max_dist=100,
#        shf_increase_factor=1).save("backgr.png")



# img = Image.open("карта.png")
# genMappingWarPic(image=img,
#                  attack_color=(255, 0, 0),
#                  defence_color=(0, 0, 255),
#                  steps=10,
#                  break_intensity=10,
#                  break_frequency=1).show()



# genCurvesBackground(img_size=2000,
#                     background_color=(0, 0, 0),
#                     lines_steps=5,
#                     line_lenght=600,
#                     lines_to_new_step=4,
#                     angle_states_change_qnty=3,
#                     angle_move_range=(-50, 50),
#                     angle_move_bias_range=(0, 0),
#                     lines_start_gradient_color=(255, 0, 255),
#                     lines_end_gradient_color=(0, 210, 0),).show()