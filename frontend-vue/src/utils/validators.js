export const fileValidators = {
  validateResumeFile(file) {
    const errors = []
    
    if (!file) {
      errors.push('Veuillez sélectionner un fichier')
      return { isValid: false, errors }
    }

    const maxSize = 10 * 1024 * 1024 // 10MB
    if (file.size > maxSize) {
      errors.push('Le fichier ne doit pas dépasser 10MB')
    }

    const allowedTypes = [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]

    if (!allowedTypes.includes(file.type)) {
      errors.push('Seuls les fichiers PDF, DOC et DOCX sont acceptés')
    }

    return {
      isValid: errors.length === 0,
      errors
    }
  },

  validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  },

  validateRequired(value) {
    return value !== null && value !== undefined && value.toString().trim() !== ''
  },

  validateLength(value, min = 0, max = Infinity) {
    const length = value?.toString().length || 0
    return length >= min && length <= max
  }
}

export const formValidators = {
  validateLoginForm(data) {
    const errors = {}
    
    if (!fileValidators.validateRequired(data.email)) {
      errors.email = 'L\'email est requis'
    } else if (!fileValidators.validateEmail(data.email)) {
      errors.email = 'L\'email n\'est pas valide'
    }

    if (!fileValidators.validateRequired(data.password)) {
      errors.password = 'Le mot de passe est requis'
    }

    return {
      isValid: Object.keys(errors).length === 0,
      errors
    }
  },

  validateRegisterForm(data) {
    const errors = {}
    
    if (!fileValidators.validateRequired(data.firstName)) {
      errors.firstName = 'Le prénom est requis'
    }

    if (!fileValidators.validateRequired(data.lastName)) {
      errors.lastName = 'Le nom est requis'
    }

    if (!fileValidators.validateRequired(data.email)) {
      errors.email = 'L\'email est requis'
    } else if (!fileValidators.validateEmail(data.email)) {
      errors.email = 'L\'email n\'est pas valide'
    }

    if (!fileValidators.validateRequired(data.password)) {
      errors.password = 'Le mot de passe est requis'
    } else if (!fileValidators.validateLength(data.password, 8)) {
      errors.password = 'Le mot de passe doit contenir au moins 8 caractères'
    }

    if (data.password !== data.confirmPassword) {
      errors.confirmPassword = 'Les mots de passe ne correspondent pas'
    }

    return {
      isValid: Object.keys(errors).length === 0,
      errors
    }
  }
}
