    #_______________________________________________________

#Esse aqui funciona, caso precise    
# async def detect_and_authorize(websocket: WebSocket, queue: asyncio.Queue):
#     '''Essa função pega a informação recebido e manda isso para o 
#     classificador, que então percorre a informação para detectar a 
#     presença de um rosto humano, retornando a localização da 
#     face numa stream de câmera contínua, já que a lista de 4 tuples 
#     representa os 4 lados do retângulo e autorizando caso o usuário0
#     exista na base de dados.'''
    
#     successful_attempts = 0
#     total_attempts = 100

#     while total_attempts > 0:
#         faces_output = []
#         bytes = await queue.get()
#         data = np.frombuffer(bytes, dtype=np.uint8)
#         img = cv2.imdecode(data, 1)
        
#         if camera_model.camera_width == 0 or camera_model.camera_height == 0:
#             height, width = img.shape[:2]
#             camera_model.update_dimensions(width, height)
        
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
#         faces = cascade_classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6, minSize=(30, 30))
        
        
#         print(f"Finding faces_______________________{len(faces)}")
#         if len(faces) > 1:
#             print("Multiples faces detected")
#             await websocket.send_json({"authenticate": False, "message": f"Multiplos rostos detectados, favor deixar apenas um usuário na tela"})
#             continue
        
#         if len(faces) > 0:   
#             rgb_image = face_model.convert_to_rgb(img)
#             face_locations = face_model.detect_faces(rgb_image)
#             print("Face locations: ", face_locations)
            
#             if not face_locations:
#                 print("Face found by Haar cascade, but no face locations detected.")
#                 total_attempts -= 1
#                 continue
            
#             camera_model.find_center_face(face_locations)
#             if not camera_model.check_if_centered():
#                 total_attempts -= 1   
#                 print("Face not centered")
#                 await websocket.send_json({"authenticate": False, "message": "Rosto não está centralizado"})
#                 continue
          
#             encoding = face_model.extract_face_encoding(rgb_image, face_locations)
        
#             if encoding is not None:
#                 label, mail, is_match = await face_controller.compare_with_db(encoding)
                
#                 #Aqui envia as coordenadas do rosto na tela e o label da pessa se essa já tiver um, senão envia como desconhecido
#                 #Essa função não seria necessária, mas o front está pegando o label dela, então vou deixar ela aqui
#                 for (x, y, w, h) in faces: 
#                     face_instance = Face(x=x, y=y, width=w, height=h, label=label)
#                     faces_output.append(face_instance)
#                 faces_list = FacesList(facesList=faces_output)
#                 #End
                
#                 if is_match:
#                     successful_attempts += 1
                    
#                     if successful_attempts >= 5:
                        
#                         #_____________________________Checking microsoft authentication
#                         try: 
#                             token_header = websocket.headers.get("sec-websocket-protocol")
#                             tokens = parse_token(token_header)

#                             user_info = decode_token(tokens["auth_token"])
#                             group_members = await fetch_group_members(tokens["auth_token"], tokens["group_token"])
#                             user_mail = user_info.get("mail")
#                             is_in_group = await is_member_in_group(group_members, user_mail)
                            
#                             if is_in_group:
#                                 print(f"Successfull attempt login. {user_mail} found in group")
#                                 await websocket.send_json({
#                                     "authenticate": True,
#                                     "label": label,
#                                     "mail": mail,
#                                     "message": f"Usuário autenticado como {label}."
#                                 })
#                                 break
                            
#                         except Exception as e:
#                             await websocket.send_json({
#                                 "authenticate": False,
#                                 "message": f"Erro durante a autenticação do grupo: {str(e)}"
#                             })
                        
#                         #_____________________________

#                 else:
#                     await websocket.send_json({"authenticate": False, "message": f"Rosto não reconhecido no banco, tentando novamente..."})
#             else:
#                 await websocket.send_json({"authenticate": False, "message": f"Nenhum encoding encontrado na imagem."})
#         else:
#             faces_list = FacesList(facesList=[])
#             await websocket.send_json({"authenticate": False, "message": f"Nenhum rosto detectado."})
            
#         await websocket.send_json(faces_list.model_dump())
        
#     total_attempts -= 1
#     print("Atintigu maximo de attemps")
#     await websocket.send_json({"error": "Reconhecimento atingiu o máximo de tentativas."})
#     return